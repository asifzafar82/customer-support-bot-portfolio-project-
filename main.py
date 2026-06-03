import os
import textwrap
from typing import List, Dict, Optional

try:
    import openai
except ImportError:
    openai = None

PROJECT_NAME = "Customer Support Prompt Engineering Bot"

SYSTEM_INSTRUCTIONS = textwrap.dedent(
    """
    You are a professional customer support assistant for a SaaS product called Acme Assist.
    Your goal is to solve customer issues quickly, clearly, and politely.
    Follow these rules:
    1. Ask clarifying questions only when needed.
    2. Keep responses concise and friendly.
    3. Use bullet points for steps and include a short summary.
    4. Confirm the user is satisfied before ending the conversation.
    5. When the user asks for examples or best practices, provide prompt engineering guidance.
    """
)

EXAMPLES = [
    {
        "role": "user",
        "content": "My app is showing error 502 when I try to log in. What should I do?"
    },
    {
        "role": "assistant",
        "content": (
            "First, clear your browser cache and retry. "
            "If the issue persists, check your network connection and attempt login again. "
            "If you still see the error, please send a screenshot of the message."
        )
    },
    {
        "role": "user",
        "content": "How can I create a better prompt for a support chatbot?"
    },
    {
        "role": "assistant",
        "content": (
            "Use a clear role definition, describe the task, include user context, and request the output format. "
            "For example: 'You are a helpful support agent. A customer reports a login failure. Provide a step-by-step checklist and troubleshooting questions.'"
        )
    }
]

CATEGORY_PROMPT = {
    "billing": "The customer asks about charges, invoices, refunds, or subscription plans.",
    "technical": "The customer reports an error, bug, or product issue requiring troubleshooting.",
    "account": "The customer needs help with login, account updates, or security questions.",
    "sales": "The customer wants feature comparisons, pricing details, or upgrade recommendations."
}

PROMPT_TIPS = [
    "Define the assistant's role explicitly.",
    "Provide one or two concise examples for the model.",
    "Ask for a structured output format when needed (e.g. bullet points, tables).",
    "Include relevant context such as product name, user goal, and issue type.",
    "Use a calm, professional tone and confirm understanding at the end."
]


def get_api_key() -> Optional[str]:
    return os.environ.get("OPENAI_API_KEY")


def build_prompt(user_message: str, category: Optional[str] = None) -> List[Dict[str, str]]:
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},
    ]

    if category and category in CATEGORY_PROMPT:
        messages.append(
            {
                "role": "system",
                "content": f"Category context: {CATEGORY_PROMPT[category]}"
            }
        )

    messages.extend(EXAMPLES)
    messages.append({"role": "user", "content": user_message})
    return messages


def summarize_prompt_design(user_message: str, category: Optional[str] = None) -> str:
    prompt_parts = [
        f"Role: customer support assistant for Acme Assist.",
        f"Task: respond to the user's issue in a clear, friendly, and practical way.",
    ]

    if category:
        prompt_parts.append(f"Issue type: {category}.")

    prompt_parts.append(f"User input: {user_message}")
    prompt_parts.append("Output style: bullet points when providing steps, short summary, polite close.")

    return " \n".join(prompt_parts)


def show_prompt_engineering_tips() -> None:
    print("\nPrompt Engineering Tips:\n")
    for idx, tip in enumerate(PROMPT_TIPS, start=1):
        print(f"{idx}. {tip}")
    print("\nExample: Use a precise role, add context, and ask for the exact format you want.")


def choose_category() -> Optional[str]:
    print("\nSelect a support category to improve intent detection:")
    for index, category in enumerate(CATEGORY_PROMPT.keys(), start=1):
        print(f"{index}. {category.title()}")
    print("0. No category")

    choice = input("Choose a category number: ").strip()
    if choice == "0":
        return None

    try:
        choice_index = int(choice) - 1
        categories = list(CATEGORY_PROMPT.keys())
        if 0 <= choice_index < len(categories):
            return categories[choice_index]
    except ValueError:
        pass

    print("Invalid choice. Continuing without category.")
    return None


def call_openai(messages: List[Dict[str, str]]) -> str:
    if openai is None:
        raise ImportError(
            "The openai package is not installed. Install it with `pip install openai`."
        )

    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. Export it in your environment before running the bot."
        )

    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=400,
        temperature=0.3,
        top_p=0.95,
    )
    return response.choices[0].message.content.strip()


def run_chat_loop() -> None:
    print(f"\n{PROJECT_NAME}")
    print("A small prompt engineering demo for customer support chatbots.\n")

    while True:
        print("Options:")
        print("1. Start a support conversation")
        print("2. Show prompt engineering tips")
        print("3. View the generated prompt design")
        print("4. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            user_message = input("\nEnter the customer's issue: ").strip()
            category = choose_category()
            messages = build_prompt(user_message, category)
            print("\n[Prompt design summary]")
            print(summarize_prompt_design(user_message, category))
            print("\n[Sending to model...]")

            try:
                reply = call_openai(messages)
                print("\nBot response:\n")
                print(reply)
            except Exception as error:
                print(f"Error: {error}")
                print("If you want to skip OpenAI, inspect the prompt design instead.")

        elif choice == "2":
            show_prompt_engineering_tips()
        elif choice == "3":
            sample = input("\nEnter a sample customer issue to preview prompt design: ").strip()
            category = choose_category()
            print("\nGenerated prompt design:\n")
            print(summarize_prompt_design(sample, category))
        elif choice == "4":
            print("Goodbye! Continue refining your prompts and support scripts.")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 4.")


if __name__ == "__main__":
    run_chat_loop()

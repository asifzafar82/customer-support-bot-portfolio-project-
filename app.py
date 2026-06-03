import streamlit as st

from main import build_prompt, summarize_prompt_design, CATEGORY_PROMPT, PROMPT_TIPS, call_openai

st.set_page_config(page_title="Customer Support Bot UI", layout="centered")
st.title("Customer Support Prompt Engineering Demo")
st.write(
    "Use this web interface to test customer issues, inspect the prompt design, and refine your prompt engineering approach."
)

user_issue = st.text_area(
    "Customer issue",
    placeholder="I can't access my account because I keep getting error 502.",
    height=180,
)
category_options = ["None"] + [cat.title() for cat in CATEGORY_PROMPT.keys()]
selected_category = st.selectbox("Support category", category_options)

if st.button("Send to model"):
    if not user_issue.strip():
        st.warning("Please enter a customer issue before sending.")
    else:
        category = None if selected_category == "None" else selected_category.lower()
        messages = build_prompt(user_issue, category)

        st.subheader("Prompt design summary")
        st.code(summarize_prompt_design(user_issue, category), language="text")

        with st.spinner("Calling OpenAI..."):
            try:
                response = call_openai(messages)
                st.subheader("Model response")
                st.write(response)
            except Exception as error:
                st.error(f"Model request failed: {error}")
                st.info("Make sure OPENAI_API_KEY is set in your environment and the openai package is installed.")

        st.subheader("Generated prompt messages")
        st.json(messages)

st.sidebar.header("Prompt engineering tips")
for tip in PROMPT_TIPS:
    st.sidebar.write(f"- {tip}")

st.sidebar.markdown(
    "---\n"
    "**Run command:** `streamlit run app.py`\n"
    "\n**Tip:** View the prompt summary first, then compare the model answer to your ideal support response."
)

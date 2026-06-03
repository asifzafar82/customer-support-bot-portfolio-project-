# Customer Support Bot Portfolio Project

This project is a Python template for a customer support chatbot that demonstrates prompt engineering skills.

## What this template shows

- A clearly defined system prompt for customer support behavior
- Example few-shot messages to shape answer style
- Category-based prompt context for better intent handling
- A prompt design summary to explain how the model is guided
- A simple console interface for experimenting and learning

## Usage

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Set your OpenAI API key:

```powershell
$env:OPENAI_API_KEY = "your_api_key_here"
```

3. Run the console bot:

```powershell
python main.py
```

4. Run the web UI:

```powershell
streamlit run app.py
```

## Prompt engineering learning

The bot lets you:

- review the prompt structure used for each query
- choose a support category to improve context
- see prompt engineering tips and examples

## Customize

Update `SYSTEM_INSTRUCTIONS`, `EXAMPLES`, and `CATEGORY_PROMPT` in `main.py` to showcase your own prompt engineering style and portfolio examples.

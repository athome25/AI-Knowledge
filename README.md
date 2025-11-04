# AI-Knowledge: Database Query Chat Interface

A Streamlit chat application that converts natural language questions into SQL queries using LangChain and Claude AI.

## Prerequisites

- Python 3.8 or higher
- Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/athome25/AI-Knowledge.git
cd AI-Knowledge
```

2. Create a virtual environment:
```bash
python -m venv venv

source venv/bin/activate    # Mac
venv\Scripts\activate       # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Setup

Copy `env.example` to `.env` file in the project root and add your Anthropic API key:
```
API_KEY=your_api_key_here
```

## Running the App

Start the Streamlit application:
```bash
streamlit run app.py
```

### Example Queries

- "Who are the 3 oldest employees"

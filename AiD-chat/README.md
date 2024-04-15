# gen-ai-hackathon

## Project #4 - FCDO monitoring and evaluation
Resources: https://no10ds.github.io/evidence-house/events/gen-ai-hack/challenges/evaluation/evaluation.html

### Our problem statement:
*"How do we use Gen AI to learn from past international development and policy projects to improve current and future projects?"*

### Running the code
First install the requirements by running pip3 install -r requirements.txt

`import_data.py` will process cleaned text data into FAISS embeddings. Running this is optional as we've also provided these files.

`run_chatbot.py` will use these embeddings and an OPENAPI api key to spin up a dashboard with the chatbot. You will need to copy `.env.example` to create `.env` and fill in your chatgpt api key, which can be found here: https://platform.openai.com/account/api-keys

When the dashboard is running, you can access it at http://127.0.0.1:8050/

After typing in your query to the chatbot, press the submit button and wait a few seconds for a response (typically less than 20)
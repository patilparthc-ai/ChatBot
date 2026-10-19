# AI Chatbot using ML APIs

Files: data.csv (dataset), generate_data.py (rebuilds the dataset), train_model.py (trains the model),
responses.py (bot answers), chatbot.py (the chatbot), chatbot.ipynb (same project for Jupyter), requirements.txt.

## Run (Anaconda Prompt / VS Code terminal)
    conda create -n chatbot_env python=3.11 -y
    conda activate chatbot_env
    pip install -r requirements.txt notebook
    python train_model.py
    python chatbot.py

## Turn on the API (answers any topic)
Get a key from aistudio.google.com, then
    Windows (PowerShell):  $env:GEMINI_API_KEY="your_key"
    Windows (cmd):         set GEMINI_API_KEY=your_key
then run `python chatbot.py` again. Never upload your key to GitHub.

# rAIgine

## Installation

### Setting project
1. git clone git@github.com:madindo/takehome_raigine.git
2. cd takehome_raigine
3. cp .env_example .env
4. open .env add the credential given
    - OPENAI_API_KEY = will be given
    - GMAIL_USERNAME = your gmail email
    - GMAIL_PASSWORD = your gmail password
    - SEND_EMAIL_TO = email address to send your invoice summary

### Setting docker
Make sure you have docker installed
1. docker build -t takehome .
2. docker run -d --name takehome_container takehome
3. docker run -it takehome /bin/bash

### Usage
After running into the docker bash
1. For manual processing = py manual.py
2. For Prompt processing = py prompt.py
    - Insert prompt to summarize all the invoice = summarize invoice_1, invoice_2, invoice_3
    - Insert prompt to summarize just 1 invoice = summarize invoice_2
3. For forecasting data = py forecasting.py
    - It will generate csv in assets/result/forecasted_production_data_reordered.csv
    - cat assets/result/forecasted_production_data_reordered.csv  - you should see forecasted data
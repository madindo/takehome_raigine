Needed to know how to extract pdf to text

```python
import pdfplumber

def extract_text_from_pdfs(pdf_files):
    extracted_text = []
    for pdf_file in pdf_files:
        with pdfplumber.open(pdf_file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'
            extracted_text.append(text)
    return extracted_text
```

Then need to find out how to summarize those extracted text using openai

```python
import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'

def summarize_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5-turbo or newer available model
            messages=[
                {"role": "system", "content": "You are an AI assistant that summarizes texts."},
                {"role": "user", "content": f"Please provide a summary for the following text:\n{text}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"An error occurred: {str(e)}"

summarized_data = [summarize_text(text) for text in pdf_texts]
```

Then need to send email
Troubleshoots : if your gmail has 2 factor auth maybe it wouldn’t work so you need to make app password

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    from_email = "your_email@example.com"
    password = "your_password"

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(message)

email_body = "\n\n".join(summarized_data)
send_email("Summarized PDF Data", email_body, "recipient@example.com")

```

Then making something that can input as prompt

```python
def handle_prompt():
    print("Welcome to the AI-Powered Prompt Handler!")
    print("Hint: You can ask me to do something like 'summarize invoice_1, invoice_2, invoice_3' or 'summarize from invoice_1 or invoice_2 or invoice_3'")
    user_prompt = input("Please enter your prompt: ")
    user_email = input("Please enter your email: ")

    if "summarize" in user_prompt.lower():
        requested_files = []
        if "invoice_1" in user_prompt.lower():
            requested_files.append("invoice_1.pdf")
        if "invoice_2" in user_prompt.lower():
            requested_files.append("invoice_2.pdf")
        if "invoice_3" in user_prompt.lower():
            requested_files.append("invoice_3.pdf")

        # Extract and summarize
        pdf_texts = extract_text_from_pdfs(requested_files)
        summarized_data = [summarize_text(text) for text in pdf_texts]

        # Email the summarized data
        email_body = "\n\n".join(summarized_data)
        send_email("Summarized Invoice", email_body, user_email)

# Example prompt
handle_prompt()
```

Task 2:
You are given a production data. Forecast the next month of the production.

1. You can add it to a new spreadsheet or combine with existing spreadsheet
2. Create a UI to visualize the results
3. If possible, dockerize the solution for easy deployment in other people's laptop

First check if reading spreadsheet is working

```python
pip install pandas

import pandas as pd

# Load the data
data = pd.read_csv('realistic_production_data.csv')

# Take a look at the first few rows
print(data.head())
```

```python
pip install statsmodels

# Select the columns to use
columns_to_use = ['date', 'machine_id', 'cycle_time', 'downtime', 'production_count']
data = data[columns_to_use]

# Convert 'date' to datetime format
data['date'] = pd.to_datetime(data['date'])

# Sort data by date and machine_id
data = data.sort_values(by=['date', 'machine_id'])

# Initialize a DataFrame to store all forecasts
all_forecasts = []

# Group the data by 'machine_id' and apply the ARIMA forecast for each machine
grouped = data.groupby('machine_id')

for machine_id, group in grouped:
    # Sort the group by date
    group = group.sort_values(by='date')

    # Train a VAR model for multivariate forecasting
    model = VAR(group[['production_count', 'cycle_time', 'downtime']])
    model_fit = model.fit(maxlags=15)

    forecast_steps = 30
    forecast = model_fit.forecast(y=group[['production_count', 'cycle_time', 'downtime']].values, steps=forecast_steps)

    # Create a new DataFrame for forecasted data
    forecast_dates = pd.date_range(start=group['date'].max() + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
    forecast_df = pd.DataFrame(forecast, columns=['production_count', 'cycle_time', 'downtime'])
    forecast_df['date'] = forecast_dates
    forecast_df['machine_id'] = machine_id

    # Append the forecast_df to the list
    all_forecasts.append(forecast_df)

# Concatenate all forecasts into a single DataFrame
forecast_result = pd.concat(all_forecasts)

# Round values for better readability
forecast_result['cycle_time'] = forecast_result['cycle_time'].round(2)
forecast_result['downtime'] = forecast_result['downtime'].round(2)
forecast_result['production_count'] = forecast_result['production_count'].round(1)

# Rearrange columns to the correct order
forecast_result = forecast_result[['date', 'machine_id', 'cycle_time', 'downtime', 'production_count']]
# Sort the forecasted data by date and machine_id
forecast_result = forecast_result.sort_values(by=['date', 'machine_id'])

# Save the forecasted data to a new CSV file with the correct column order
forecast_result.to_csv('assets/result/forecasted_production_data_reordered.csv', index=False)

```

Setup docker

```
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies from requirements.txt or using pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the environment variables from the .env file
ENV PYTHONUNBUFFERED 1

```

```
docker build -t takehome .
docker run -it takehome /bin/bash
```
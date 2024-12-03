import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

        print("Summarized text : ")
        print(response['choices'][0]['message']['content'].strip())
        print("\n\n")

        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"An error occurred: {str(e)}"

def send_email(subject, body, to_email):
    from_email = os.getenv('GMAIL_USERNAME')
    password = os.getenv('GMAIL_PASSWORD')

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    print('Sending Email with body :')
    print(body)
    print("\n\n")

    # Send the email using smtplib
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(message)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

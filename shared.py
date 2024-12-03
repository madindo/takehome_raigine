import pdfplumber
import openai
import os
import re
from dotenv import load_dotenv
import webbrowser
import urllib.parse

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_text_from_pdfs(pdf_files):
    extracted_text = []
    for pdf_file in pdf_files:
        with pdfplumber.open(pdf_file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'
            extracted_text.append(text)

    # print("Extracted Text : ")
    # print(extracted_text)
    # print("\n\n")

    return extracted_text

def parse_invoice(invoice_text):
    # Define regex patterns for each field
    patterns = {
        "invoice_number": r"Invoice Number:\s*(.+)",
        "company_name": r"Company Name:\s*(.+)",
        "date": r"Date:\s*(.+)",
        "amount": r"Amount:\s*\$([\d,]+)",
        "details": r"Details:\s*(.+)"
    }

    parsed_data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, invoice_text)
        if match:
            parsed_data[key] = match.group(1).strip()

    return parsed_data

def scan_data(user_prompt):
    folder_path = "assets/data/"
    files = os.listdir(folder_path)
    requested_files = []
    if os.path.exists(folder_path):
        for file_name in files:
            # get single file
            base_name = os.path.splitext(file_name.lower())[0]
            if base_name in user_prompt.lower():
                requested_files.append(os.path.join(folder_path, file_name))

        if 'last' in user_prompt.lower():
            match = re.search(r"last (\d+)", user_prompt.lower())
            num_invoices = int(match.group(1)) if match else 2
            for file_name in files:
                pdf_files = [file_name for file_name in files if file_name.lower().endswith(".pdf")]
                pdf_files.sort()  # Ensure the files are sorted
                requested_files = [os.path.join(folder_path, file_name) for file_name in pdf_files[-num_invoices:]]

        # get all file with pdf
        if not requested_files:
            for file_name in files:
                if file_name.lower().endswith(".pdf"):
                    requested_files.append(os.path.join(folder_path, file_name))
    else:
        print(f"The folder '{folder_path}' does not exist.")
    return requested_files

def summarize_invoices(invoices):
    summary = {
        "total_invoices": len(invoices),
        "total_amount": 0,
        "company_summary": {}
    }
    for invoice in invoices:
        # Add to the total_amount (convert to numeric, removing commas)
        amount = float(invoice["amount"].replace(",", ""))
        summary["total_amount"] += amount

        # Summarize by company
        company_name = invoice["company_name"]
        if company_name not in summary["company_summary"]:
            summary["company_summary"][company_name] = {
                "invoices": 0,
                "total_amount": 0
            }
        summary["company_summary"][company_name]["invoices"] += 1
        summary["company_summary"][company_name]["total_amount"] += amount

    # Format the total_amount to two decimal places
    summary["total_amount"] = round(summary["total_amount"], 2)

    return summary

def format_email_body(summary):
    # Email header
    email_body = "Dear Team,\n\nHere is the summary of the invoices:\n\n"

    # General summary
    email_body += f"Total Invoices: {summary['total_invoices']}\n"
    email_body += f"Total Amount: ${summary['total_amount']:,}\n\n"

    # Company-specific summary
    email_body += "Breakdown by Company:\n"
    for company, data in summary["company_summary"].items():
        email_body += f"- {company}:\n"
        email_body += f"  - Invoices: {data['invoices']}\n"
        email_body += f"  - Total Amount: ${data['total_amount']:,}\n"

    # Closing message
    email_body += "\nBest regards,\nYour Finance Team"

    return email_body

def send_email_with_default_client(recipient, subject, body):
    # URL encode the subject and body
    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body)

    # Construct the mailto URL
    mailto_link = f"mailto:{recipient}?subject={subject_encoded}&body={body_encoded}"
    print(mailto_link)
    # Open the default email client
    webbrowser.open(mailto_link)

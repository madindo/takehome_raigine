from shared import extract_text_from_pdfs, parse_invoice, scan_data, summarize_invoices, format_email_body, send_email_with_default_client
import os

def handle_prompt():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the AI-Powered Prompt Handler!")
    print("Hint: You can ask me to do something like 'summarize invoice_1, invoice_2, invoice_3' or 'summarize all' or 'give me the sum of all invoice' or 'give me last 2 invoice'")
    user_prompt = input("Please enter your prompt: ")

    data = scan_data(user_prompt)
    pdf_texts = extract_text_from_pdfs(data)
    structured_data = [parse_invoice(invoice) for invoice in pdf_texts]

    if any(keyword in user_prompt.lower() for keyword in ["summarize", "last"]):
        summary = summarize_invoices(structured_data)
        email_body = format_email_body(summary)
        user_email = input("Please enter your email: ")
        send_email_with_default_client(user_email, "Summary Invoice", email_body)
    if "sum" in user_prompt.lower():
        total = sum(float(item["amount"].replace(",", "")) for item in structured_data)
        print("Total Amount:" , total);

handle_prompt()

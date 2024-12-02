from shared import extract_text_from_pdfs, summarize_text, send_email

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
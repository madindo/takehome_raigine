from shared import extract_text_from_pdfs, summarize_text, send_email
from dotenv import load_dotenv

load_dotenv()

# extract
pdf_files = ["assets/data/invoice_1.pdf", "assets/data/invoice_2.pdf", "assets/data/invoice_3.pdf"]
pdf_texts = extract_text_from_pdfs(pdf_files)

# summarize
summarized_data = [summarize_text(text) for text in pdf_texts]

# email summarized data
email_body = "\n\n".join(summarized_data)
send_email("Summary Invoice ", email_body, os.getenv('SEND_EMAIL_TO'))

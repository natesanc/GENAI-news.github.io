import PyPDF2

def extract_pdf_to_txt(pdf_path,txt_path):
    with open(pdf_path,'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for pages in reader.pages:
            text += pages.extract_text() or ""
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

file_path = r"C:\Users\nates\OneDrive\Desktop\gen ai\GenAI\KB\asset\The Economic Times Bangalore 27 10 2025.pdf"
file_save_path = r"C:\Users\nates\OneDrive\Desktop\gen ai\GenAI\KB\asset\27-10-2025-ET.txt"

extract_pdf_to_txt(file_path, file_save_path)
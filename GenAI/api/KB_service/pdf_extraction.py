import os
import PyPDF2

def extract_pdf_to_txt(pdf_path, txt_path):
    try:
        # ✅ 1. Ensure the output directory exists
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)

        # ✅ 2. Open and read the PDF
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)

            # ✅ 3. Handle encrypted PDFs gracefully
            if reader.is_encrypted:
                try:
                    reader.decrypt("")  # try without password
                except Exception:
                    raise Exception("PDF is encrypted and cannot be read without a password.")

            # ✅ 4. Extract text from all pages
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

        # ✅ 5. Save extracted text
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        return text

    except Exception as e:
        raise Exception(f"Error during PDF extraction: {e}")

    
if __name__ == "__main__":
    file_path = r"C:\Users\mhema\OneDrive\Documents\GenAI\GenAIProject\KB Creation\assets\27-10-2025-ET.pdf"
    file_save_path = r"KB Creation\assets\27-10-2025-ET.txt"

    extract_pdf_to_txt(file_path, file_save_path)
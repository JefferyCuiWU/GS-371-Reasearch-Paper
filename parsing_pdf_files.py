import fitz
import re

def extract_hs_codes_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    hs_codes = set()  # Using a set to avoid duplicates

    # Regular expression to find HS codes (assuming they are 8 digits long)
    hs_code_pattern = re.compile(r'\b\d{8}\b')

    # Iterate through each page in the PDF
    for page in doc:
        text = page.get_text()
        # Find all HS codes on the current page
        found_codes = hs_code_pattern.findall(text)
        # Extract the first 6 digits and add to the set
        for code in found_codes:
            hs_codes.add(code[:6])  # Only take the first 6 digits

    doc.close()  # Close the document
    return list(hs_codes)  # Convert set to list if needed

pdf_path = 'list 4-2.pdf' # Change the file path accordingly
hs_codes = extract_hs_codes_from_pdf(pdf_path)
print(hs_codes)

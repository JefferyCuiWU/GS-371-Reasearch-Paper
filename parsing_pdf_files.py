import fitz
import re

def extract_hs_codes_from_pdf_ordered(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    hs_codes = []  # Using a list to maintain order

    # Regular expression to find HS codes (assuming they are 8 digits long)
    hs_code_pattern = re.compile(r'\b\d{8}\b')

    # Iterate through each page in the PDF
    for page in doc:
        text = page.get_text()
        # Find all HS codes on the current page
        found_codes = hs_code_pattern.findall(text)
        # Extract the first 6 digits and add to the list if not already included
        for code in found_codes:
            short_code = code[:6]  # Only take the first 6 digits
            if short_code not in hs_codes:
                hs_codes.append(short_code)

    doc.close()  # Close the document
    return hs_codes

pdf_path = 'Data\Lists of Goods China had Additional Tariffs on\list 4-2.pdf' # Change the file path accordingly
hs_codes = extract_hs_codes_from_pdf_ordered(pdf_path)
print(hs_codes)

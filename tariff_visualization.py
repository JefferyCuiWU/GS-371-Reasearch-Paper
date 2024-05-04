import re
import pandas as pd
from docx import Document

def extract_hs_codes_and_tariffs(docx_path):
    doc = Document(docx_path)
    data = []
    tariff_pattern = re.compile(r'(\d+\.?\d*)%:')  # Look for decimal or whole number percentage followed by colon
    hs_code_pattern = re.compile(r"'\d{6}'")  # Pattern to match HS codes exactly six digits within quotes
    current_wave = ""
    current_year = 0
    wave_year_mapping = {
        "China’s Announcement to WTO": 2018,
        "China’s Retaliatory Tariffs List 1": 2018,
        "China’s Retaliatory Tariffs List 2": 2019,
        "China’s Retaliatory Tariffs List 3": 2019,
        "China’s Retaliatory Tariffs List 4": 2020
    }

    for para in doc.paragraphs:
        # Check if the paragraph is naming a wave and set current_wave and current_year
        if any(wave in para.text for wave in wave_year_mapping):
            current_wave = para.text.strip()
            current_year = wave_year_mapping.get(current_wave, 0)
        # Search for tariff percentage in the paragraph text
        tariff_match = tariff_pattern.search(para.text)
        if tariff_match:
            tariff_rate = float(tariff_match.group(1))  # Convert to float to accommodate decimal tariffs
            # Extract all HS codes in the paragraph
            hs_codes = hs_code_pattern.findall(para.text)
            for code in hs_codes:
                hs_code = code.strip("'")
                data.append({'HS 6': hs_code, 'Tariff Increase (%)': tariff_rate, 'Wave': current_wave, 'Year': current_year})

    return pd.DataFrame(data)

def save_data_to_excel(data, file_name):
    # Save DataFrame to Excel
    data.to_excel(file_name, index=False)

# Usage
data = extract_hs_codes_and_tariffs('Data\Lists of Goods China had Additional Tariffs on\Goods with Additional Tariffs by HS 6 codes and Retaliatory Lists.docx')
save_data_to_excel(data, 'Results/products_tariffs.xlsx')

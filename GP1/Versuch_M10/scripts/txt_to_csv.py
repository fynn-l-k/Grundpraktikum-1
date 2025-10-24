import csv
import os

def txt_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    # Replace commas with dots and split by tab or whitespace
    processed_lines = []
    for line in lines:
        line = line.replace(',', '.')  # replace decimal comma with dot
        line = line.strip()
        if line:
            # split by tab or whitespace
            parts = line.split('\t') if '\t' in line else line.split()
            processed_lines.append(parts)
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(processed_lines)

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            input_file = os.path.join(folder_path, filename)
            output_file = os.path.join('/Users/fynnlucca/Documents/Grundpraktikum-1/Versuch_M10/M10_Aufgabe_1_CSV_Daten', filename.replace('.txt', '.csv'))
            print(f"Processing {input_file} → {output_file}")
            txt_to_csv(input_file, output_file)

#for file in os.listdir('/Users/fynnlucca/Documents/Grundpraktikum-1/Versuch_/M10_Aufgabe_1_Daten'):
txt_to_csv('/Users/fynnlucca/Documents/Grundpraktikum-1/Versuch_H2/Data_Blaue_Kugel.txt', '/Users/fynnlucca/Documents/Grundpraktikum-1/Versuch_H2/Data_Blaue_Kugel.csv')

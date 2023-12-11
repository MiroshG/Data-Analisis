import fitz
import os
import mysql.connector

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='boxing_data'
)


############################################# LOOP TO RUN OVER ALL THE PDFS ##############################

pdf_start='C:\\Users\\Mirosh\\Desktop\\Data\\'

# List of weights to navigate through
sex_boxers = ['H', 'M']

for weight in sex_boxers:

    weight_path = os.path.join(pdf_start, weight)
    
    for dirpath, _, phases_of_event in os.walk(weight_path):

        for number_of_match in phases_of_event:

            if number_of_match.endswith('.pdf'):

                file_path = os.path.join(dirpath, number_of_match)

                try:
                    pdf_document = fitz.open(file_path)
                    
                    # Process the PDF (e.g., extract text)
                    for page_num in range(pdf_document.page_count):

                        page = pdf_document.load_page(page_num)
                        text = page.get_text("text")
                        print(f"Text from {number_of_match} - Page {page_num + 1}:\n{text}\n")
                        
                    pdf_document.close()  # Close the PDF file

                except Exception as e:

                    print(f"Error processing {number_of_match}: {e}")



# Example data to be inserted into tables
data_for_table1 = [(1, 'Alice', 25), (2, 'Bob', 30)]
data_for_table2 = [(1, 'Charlie', 'example1'), (2, 'David', 'example2')]
data_for_table3 = [(1, 'Eva', 'data1'), (2, 'Frank', 'data2')]
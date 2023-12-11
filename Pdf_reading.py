import fitz
import os
import mysql.connector
import tabula

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='boxing_data'
)

# DICTIONARY ##

Dictionary_boxing = {"gender":"",
                     "weight":"",
                     "fase of competition":"",
                     "Name red boxer":"",
                     "Name blue boxer":"",
                     "Winner":"",
                     "Decision":"",
 ############################### SECOND ROUND #####################                    
                     "Round 1 red judge 1":"",
                     "Round 1 blue judge 1":"",
                     "Round 1 red judge 2":"",
                     "Round 1 blue judge 2":"",
                     "Round 1 red judge 3":"",
                     "Round 1 blue judge 3":"",
                     "Round 1 red judge 4":"",
                     "Round 1 blue judge 4":"",
                     "Round 1 red judge 5":"",
                     "Round 1 blue judge 5":"",
                     "Warnings red":"",
                     "Warnings blue":"",
                     "Knockdown red":"",
                     "Knockdown blue":"",
############################### SECOND ROUND #####################
                     "Round 2 red judge 1":"",
                     "Round 2 blue judge 1":"",
                     "Round 2 red judge 2":"",
                     "Round 2 blue judge 2":"",
                     "Round 2 red judge 3":"",
                     "Round 2 blue judge 3":"",
                     "Round 2 red judge 4":"",
                     "Round 2 blue judge 4":"",
                     "Round 2 red judge 5":"",
                     "Round 2 blue judge 5":"",
                     "Warnings red":"",
                     "Warnings bluee":"",
                     "Knockdown red":"",
                     "Knockdown blue":"",
############################### THIRD ROUND #######################
                     "Round 3 red judge 1":"",
                     "Round 3 blue judge 1":"",
                     "Round 3 red judge 2":"",
                     "Round 3 blue judge 2":"",
                     "Round 3 red judge 3":"",
                     "Round 3 blue judge 3":"",
                     "Round 3 red judge 4":"",
                     "Round 3 blue judge 4":"",
                     "Round 3 red judge 5":"",
                     "Round 3 blue judge 5":"",
                     "Warnings red":"",
                     "Warnings bluee":"",
                     "Knockdown red":"",
                     "Knockdown blue":"",
############################### TOTAL POINTS #######################
                     "Total points red judge 1":"",
                     "Total points blue judge 1":"",
                     "Total points red judge 2":"",
                     "Total points blue judge 2":"",
                     "Total points red judge 3":"",
                     "Total points blue judge 3":"",
                     "Total points red judge 4":"",
                     "Total points blue judge 4":"",
                     "Total points red judge 5":"",
                     "Total points blue judge 5":"",
                     "Total Warnings red":"",
                     "Total Warnings bluee":"",
                     "Total Knockdown red":"",
                     "Total Knockdown blue":"",
####################################################################
                     "Referee":"",
                     "Judge 1":"",
                     "Nationality Judge 1":"",
                     "Judge 2":"",
                     "Nationality Judge 2":"",
                     "Judge 3":"",
                     "Nationality Judge 3":"",
                     "Judge 4":"",
                     "Nationality Judge 4":"",
                     "Judge 5":"",
                     "Nationality Judge 5":"",
                    }
Dictionary_birth_date = {}

#Dictionary_birth_date[Name_of_the_boxer]= birth_date


############################################# LOOP TO RUN OVER ALL THE PDFS ##############################

pdf_start='C:\\Users\\Mirosh\\Desktop\\Data\\'

# List of weights to navigate through
#gender_boxers = ['H', 'M']
gender_boxers=['H2']

for weight in gender_boxers:

    weight_path = os.path.join(pdf_start, weight)
    
    for dirpath, _, phases_of_event in os.walk(weight_path):

        for number_of_match in phases_of_event:

            if number_of_match.endswith('.pdf') and number_of_match != "Entry_list.pdf":

                file_path = os.path.join(dirpath, number_of_match)


                # Read tables from the PDF
                tables = tabula.read_pdf(file_path, pages='all')
                
                print(tables)

                try:
                    pdf_document = fitz.open(file_path)
                    
                    # Process the PDF (e.g., extract text)
                    for page_num in range(pdf_document.page_count):

                        page = pdf_document.load_page(page_num)
                        text = page.get_text("text")
                        

                        # REGULAR EXPRESSIONS IN THE FOLLOWING LINES: ################
                        print(f"Text from {number_of_match} - Page {page_num + 1}:{text}")
                        
                    pdf_document.close()  # Close the PDF file

                except Exception as e:

                    print(f"Error processing {number_of_match}: {e}")
                    
            elif number_of_match == "Entry_list.pdf":

                file_path = os.path.join(dirpath, number_of_match)

                try:
                    pdf_document = fitz.open(file_path)
                    
                    # Process the PDF (e.g., extract text)
                    for page_num in range(pdf_document.page_count):

                        page = pdf_document.load_page(page_num)
                        text = page.get_text("text")
                        

                        # REGULAR EXPRESSIONS IN THE FOLLOWING LINES: ################
                        print(f"Text from {number_of_match} - Page {page_num + 1}:{text}")
                        
                    pdf_document.close()  # Close the PDF file

                except Exception as e:

                    print(f"Error processing {number_of_match}: {e}")





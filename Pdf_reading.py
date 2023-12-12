import fitz
import os
import mysql.connector
import tabula
import re

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
                     "phase of competition":"",
                     "Name red boxer":"",
                     "Nationality red boxer":"",
                     "Name blue boxer":"",
                     "Nationality blue boxer":"",
                     "Winner":"",
                     "Result":"",
                     "Decision":"",
 ############################### FIRST ROUND #####################                    
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
                     "Warnings red Round 1":"",
                     "Warnings blue Round 1":"",
                     "Knockdown red Round 1":"",
                     "Knockdown blue Round 1":"",
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
                     "Warnings red Round 2":"",
                     "Warnings blue Round 2":"",
                     "Knockdown red Round 2":"",
                     "Knockdown blue Round 2":"",
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
                     "Warnings red Round 3":"",
                     "Warnings blue Round 3":"",
                     "Knockdown red Round 3":"",
                     "Knockdown blue Round 3":"",
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
                     "Total Warnings blue":"",
                     "Total Knockdown red":"",
                     "Total Knockdown blue":"",
####################################################################
                     "Referee":"",
                     "Referee nationality":"",
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

                print(len(tables[0]))
                print(tables)

                ##################################################################################################################
                ##############################            DATA FROM THE TABLE OF THE MATCH           #############################
                ##################################################################################################################

                # ROUND 1 ###################################

                judge_1_round_1=tables[0].iloc[3, 1]
                judge_2_round_1=tables[0].iloc[3, 2]
                judge_3_round_1=tables[0].iloc[3, 3]
                judge_4_round_1=tables[0].iloc[3, 4]
                judge_5_round_1=tables[0].iloc[3, 5]

                if isinstance(judge_1_round_1, str):
                    Round_1_red_judge_1 , Round_1_blue_judge_1 = judge_1_round_1.split()
                    Round_1_red_judge_2 , Round_1_blue_judge_2 = judge_2_round_1.split()
                    Round_1_red_judge_3 , Round_1_blue_judge_3 = judge_3_round_1.split()
                    Round_1_red_judge_4 , Round_1_blue_judge_4 = judge_4_round_1.split()
                    Round_1_red_judge_5 , Round_1_blue_judge_5 = judge_5_round_1.split()

                    Dictionary_boxing["Round 1 red judge 1"]=Round_1_red_judge_1
                    Dictionary_boxing["Round 1 blue judge 1"]=Round_1_blue_judge_1
                    Dictionary_boxing["Round 1 red judge 2"]=Round_1_red_judge_2
                    Dictionary_boxing["Round 1 blue judge 2"]=Round_1_blue_judge_2
                    Dictionary_boxing["Round 1 red judge 3"]=Round_1_red_judge_3
                    Dictionary_boxing["Round 1 blue judge 3"]=Round_1_blue_judge_3
                    Dictionary_boxing["Round 1 red judge 4"]=Round_1_red_judge_4
                    Dictionary_boxing["Round 1 blue judge 4"]=Round_1_blue_judge_4
                    Dictionary_boxing["Round 1 red judge 5"]=Round_1_red_judge_5
                    Dictionary_boxing["Round 1 blue judge 5"]=Round_1_blue_judge_5

                # ROUND 2 ###################################

                if len(tables[0])>= 5+1:
                    judge_1_round_2=tables[0].iloc[4, 1]
                    judge_2_round_2=tables[0].iloc[4, 2]
                    judge_3_round_2=tables[0].iloc[4, 3]
                    judge_4_round_2=tables[0].iloc[4, 4]
                    judge_5_round_2=tables[0].iloc[4, 5]

                    if isinstance(judge_1_round_2, str):
                        Round_2_red_judge_1 , Round_2_blue_judge_1 = judge_1_round_2.split()
                        Round_2_red_judge_2 , Round_2_blue_judge_2 = judge_2_round_2.split()
                        Round_2_red_judge_3 , Round_2_blue_judge_3 = judge_3_round_2.split()
                        Round_2_red_judge_4 , Round_2_blue_judge_4 = judge_4_round_2.split()
                        Round_2_red_judge_5 , Round_2_blue_judge_5 = judge_5_round_2.split()
                    
                        Dictionary_boxing["Round 2 red judge 1"]=Round_2_red_judge_1
                        Dictionary_boxing["Round 2 blue judge 1"]=Round_2_blue_judge_1
                        Dictionary_boxing["Round 2 red judge 2"]=Round_2_red_judge_2
                        Dictionary_boxing["Round 2 blue judge 2"]=Round_2_blue_judge_2
                        Dictionary_boxing["Round 2 red judge 3"]=Round_2_red_judge_3
                        Dictionary_boxing["Round 2 blue judge 3"]=Round_2_blue_judge_3
                        Dictionary_boxing["Round 2 red judge 4"]=Round_2_red_judge_4
                        Dictionary_boxing["Round 2 blue judge 4"]=Round_2_blue_judge_4
                        Dictionary_boxing["Round 2 red judge 5"]=Round_2_red_judge_5
                        Dictionary_boxing["Round 2 blue judge 5"]=Round_2_blue_judge_5

                # ROUND 3 ###################################

                if len(tables[0])>= 6+1:
                    judge_1_round_3=tables[0].iloc[5, 1]
                    judge_2_round_3=tables[0].iloc[5, 2]
                    judge_3_round_3=tables[0].iloc[5, 3]
                    judge_4_round_3=tables[0].iloc[5, 4]
                    judge_5_round_3=tables[0].iloc[5, 5]

                    if isinstance(judge_1_round_3, str):
                        Round_3_red_judge_1 , Round_3_blue_judge_1 = judge_1_round_3.split()
                        Round_3_red_judge_2 , Round_3_blue_judge_2 = judge_2_round_3.split()
                        Round_3_red_judge_3 , Round_3_blue_judge_3 = judge_3_round_3.split()
                        Round_3_red_judge_4 , Round_3_blue_judge_4 = judge_4_round_3.split()
                        Round_3_red_judge_5 , Round_3_blue_judge_5 = judge_5_round_3.split()

                        Dictionary_boxing["Round 3 red judge 1"]=Round_3_red_judge_1
                        Dictionary_boxing["Round 3 blue judge 1"]=Round_3_blue_judge_1
                        Dictionary_boxing["Round 3 red judge 2"]=Round_3_red_judge_2
                        Dictionary_boxing["Round 3 blue judge 2"]=Round_3_blue_judge_2
                        Dictionary_boxing["Round 3 red judge 3"]=Round_3_red_judge_3
                        Dictionary_boxing["Round 3 blue judge 3"]=Round_3_blue_judge_3
                        Dictionary_boxing["Round 3 red judge 4"]=Round_3_red_judge_4
                        Dictionary_boxing["Round 3 blue judge 4"]=Round_3_blue_judge_4
                        Dictionary_boxing["Round 3 red judge 5"]=Round_3_red_judge_5
                        Dictionary_boxing["Round 3 blue judge 5"]=Round_3_blue_judge_5

                # TOTAL ###################################

                if len(tables[0])== 6+1:
                    judge_1_total=tables[0].iloc[6, 1]
                    judge_2_total=tables[0].iloc[6, 2]
                    judge_3_total=tables[0].iloc[6, 3]
                    judge_4_total=tables[0].iloc[6, 4]
                    judge_5_total=tables[0].iloc[6, 5]
                elif len(tables[0])== 5+1:
                    judge_1_total=tables[0].iloc[5, 1]
                    judge_2_total=tables[0].iloc[5, 2]
                    judge_3_total=tables[0].iloc[5, 3]
                    judge_4_total=tables[0].iloc[5, 4]
                    judge_5_total=tables[0].iloc[5, 5]
                elif len(tables[0])== 4+1:
                    judge_1_total=tables[0].iloc[4, 1]
                    judge_2_total=tables[0].iloc[4, 2]
                    judge_3_total=tables[0].iloc[4, 3]
                    judge_4_total=tables[0].iloc[4, 4]
                    judge_5_total=tables[0].iloc[4, 5]

                if isinstance(judge_1_total, str):
                    Total_red_judge_1 , Total_blue_judge_1 = judge_1_total.split()
                    Total_red_judge_2 , Total_blue_judge_2 = judge_2_total.split()
                    Total_red_judge_3 , Total_blue_judge_3 = judge_3_total.split()
                    Total_red_judge_4 , Total_blue_judge_4 = judge_4_total.split()
                    Total_red_judge_5 , Total_blue_judge_5 = judge_5_total.split()

                    Dictionary_boxing["Total points red judge 1"]=Total_red_judge_1
                    Dictionary_boxing["Total points blue judge 1"]=Total_blue_judge_1
                    Dictionary_boxing["Total points red judge 2"]=Total_red_judge_2
                    Dictionary_boxing["Total points blue judge 2"]=Total_blue_judge_2
                    Dictionary_boxing["Total points red judge 3"]=Total_red_judge_3
                    Dictionary_boxing["Total points blue judge 3"]=Total_blue_judge_3
                    Dictionary_boxing["Total points red judge 4"]=Total_red_judge_4
                    Dictionary_boxing["Total points blue judge 4"]=Total_blue_judge_4
                    Dictionary_boxing["Total points red judge 5"]=Total_red_judge_5
                    Dictionary_boxing["Total points blue judge 5"]=Total_blue_judge_5

                # WARNINGS ##################################

                warning_round_1=tables[0].iloc[3, 6]

                if len(tables[0])== 6+1:
                    warning_round_2=tables[0].iloc[4, 6]
                    warning_round_3=tables[0].iloc[5, 6]
                    warning_total=tables[0].iloc[6, 6]

                    # Round 2 #
                    if isinstance(warning_round_2, str) and " " in warning_round_2:
                        warning_round_2_red, warning_round_2_blue = warning_round_2.split()
                        Dictionary_boxing["Warnings red Round 2"]=warning_round_2_red
                        Dictionary_boxing["Warnings blue Round 2"]=warning_round_2_blue
                    elif isinstance(warning_round_2, str):
                        Dictionary_boxing["Warnings red Round 2"]="problem"
                        Dictionary_boxing["Warnings blue Round 2"]="problem"

                    # Round 3 #
                    if isinstance(warning_round_3, str) and " " in warning_round_3:
                        warning_round_3_red, warning_round_3_blue = warning_round_3.split()
                        Dictionary_boxing["Warnings red Round 3"]=warning_round_3_red
                        Dictionary_boxing["Warnings blue Round 3"]=warning_round_3_blue
                    elif isinstance(warning_round_3, str):
                        Dictionary_boxing["Warnings red Round 3"]="problem"
                        Dictionary_boxing["Warnings blue Round 3"]="problem"


                elif len(tables[0])== 5+1:
                    warning_round_2=tables[0].iloc[4, 6]
                    warning_total=tables[0].iloc[5, 6]

                    # Round 2 #
                    if isinstance(warning_round_2, str) and " " in warning_round_2:
                        warning_round_2_red, warning_round_2_blue = warning_round_2.split()
                        Dictionary_boxing["Warnings red Round 2"]=warning_round_2_red
                        Dictionary_boxing["Warnings blue Round 2"]=warning_round_2_blue
                    elif isinstance(warning_round_2, str):
                        Dictionary_boxing["Warnings red Round 2"]="problem"
                        Dictionary_boxing["Warnings blue Round 2"]="problem"

                elif len(tables[0])== 4+1:
                    warning_total=tables[0].iloc[4, 6]

                # Round 1 #
                if isinstance(warning_round_1, str) and " " in warning_round_1:
                    warning_round_1_red, warning_round_1_blue = warning_round_1.split()
                    Dictionary_boxing["Warnings red Round 1"]=warning_round_1_red
                    Dictionary_boxing["Warnings blue Round 1"]=warning_round_1_blue
                elif isinstance(warning_round_1, str):
                    Dictionary_boxing["Warnings red Round 1"]="problem"
                    Dictionary_boxing["Warnings blue Round 1"]="problem"

                # Total #
                if isinstance(warning_total, str) and " " in warning_total:
                    warning_total_red, warning_total_blue = warning_total.split()
                    Dictionary_boxing["Total Warnings red"]=warning_total_red
                    Dictionary_boxing["Total Warnings blue"]=warning_total_blue
                elif isinstance(warning_total, str):
                    Dictionary_boxing["Total Warnings red"]="problem"
                    Dictionary_boxing["Total Warnings blue"]="problem"

                # KNOCKDOWNS #################################

                knockdown_round_1=tables[0].iloc[3, 7]

                if len(tables[0])== 6+1:
                    
                    knockdown_round_2=tables[0].iloc[4, 7]
                    knockdown_round_3=tables[0].iloc[5, 7]
                    knockdown_total=tables[0].iloc[6, 7]

                    # Round 2 #
                    if isinstance(knockdown_round_2, str) and " " in knockdown_round_2: 
                        knockdown_round_2_red, knockdown_round_2_blue = knockdown_round_2.split()
                        Dictionary_boxing["Knockdown red Round 2"]=knockdown_round_2_red
                        Dictionary_boxing["Knockdown blue Round 2"]=knockdown_round_2_blue
                    elif isinstance(knockdown_round_2, str):
                        Dictionary_boxing["Knockdown red Round 2"]="problem"
                        Dictionary_boxing["Knockdown blue Round 2"]="problem"

                    # Round 3 #
                    if isinstance(knockdown_round_3, str) and " " in knockdown_round_3:
                        knockdown_round_3_red, knockdown_round_3_blue = knockdown_round_3.split()
                        Dictionary_boxing["Knockdown red Round 3"]=knockdown_round_3_red
                        Dictionary_boxing["Knockdown blue Round 3"]=knockdown_round_3_blue
                    elif isinstance(knockdown_round_3, str):
                        Dictionary_boxing["Knockdown red Round 3"]="problem"
                        Dictionary_boxing["Knockdown blue Round 3"]="problem"
                
                elif len(tables[0])== 5+1:
                    knockdown_round_2=tables[0].iloc[4, 7]
                    knockdown_total=tables[0].iloc[5, 7]

                    # Round 2 #
                    if isinstance(knockdown_round_2, str) and " " in knockdown_round_2: 
                        knockdown_round_2_red, knockdown_round_2_blue = knockdown_round_2.split()
                        Dictionary_boxing["Knockdown red Round 2"]=knockdown_round_2_red
                        Dictionary_boxing["Knockdown blue Round 2"]=knockdown_round_2_blue
                    elif isinstance(knockdown_round_2, str):
                        Dictionary_boxing["Knockdown red Round 2"]="problem"
                        Dictionary_boxing["Knockdown blue Round 2"]="problem"
                
                elif len(tables[0])== 4+1:
                    knockdown_total=tables[0].iloc[4, 7]

                # Round 1 #
                if isinstance(knockdown_round_1, str) and " " in knockdown_round_1:
                    knockdown_round_1_red, knockdown_round_1_blue = knockdown_round_1.split()
                    Dictionary_boxing["Knockdown red Round 1"]=knockdown_round_1_red
                    Dictionary_boxing["Knockdown blue Round 1"]=knockdown_round_1_blue
                elif isinstance(knockdown_round_1, str):
                    Dictionary_boxing["Knockdown red Round 1"]="problem"
                    Dictionary_boxing["Knockdown blue Round 1"]="problem"
                
                # Total #
                if isinstance(knockdown_total, str) and " " in knockdown_total:
                    knockdown_total_red, knockdown_total_blue = knockdown_total.split()
                    Dictionary_boxing["Total Knockdown red"]=knockdown_total_red
                    Dictionary_boxing["Total Knockdown blue"]=knockdown_total_blue
                elif isinstance(knockdown_total, str):
                    Dictionary_boxing["Total Knockdown red"]="problem"
                    Dictionary_boxing["Total Knockdown blue"]="problem"
                


                ##################################################################################################################
                ##############################         DATA OF THE PARTICIPANTS OF THE MATCH         #############################
                ##################################################################################################################


                try:
                    pdf_document = fitz.open(file_path)
                    
                    # Process the PDF (e.g., extract text)
                    for page_num in range(pdf_document.page_count):

                        page = pdf_document.load_page(page_num)
                        text = page.get_text("text")
                        lines=text.split('\n')  # necessary to obtain some of the text
                        
                        #print(f"Text from {number_of_match} - Page {page_num + 1}:{text}")

                        # REGULAR EXPRESSIONS IN THE FOLLOWING LINES: ################
                        

                        gender_text= re.search(r"(MEN|WOMEN)'S", text)
                        weight_text= re.search(r"(\d+)kg", text)
                        phase= lines[2].strip()

                        red_boxer= lines[19].strip()
                        red_boxer_nationality=lines[20].strip()

                        blue_boxer= lines[21].strip()
                        blue_boxer_nationality=lines[22].strip()

                        winner= lines[23].strip()
                        result= lines[24].strip()
                        decision= lines[25].strip() 

                        referee_text= re.search(r"Referee:\n(.+?)\n", text)
                        referee_nationality_text=re.search(r"(.+)(?=\nJudge 1:)", text)

                        judge_1_text= re.search(r"Judge 1:\n(.+?)\n", text)
                        nationality_judge_1= lines[27].strip()

                        judge_2_text= re.search(r"Judge 2:\n(.+?)\n", text)
                        nationality_judge_2= lines[29].strip()

                        judge_3_text= re.search(r"Judge 3:\n(.+?)\n", text)
                        nationality_judge_3= lines[31].strip()

                        judge_4_text= re.search(r"Judge 4:\n(.+?)\n", text)
                        nationality_judge_4= lines[33].strip()

                        judge_5_text= re.search(r"Judge 5:\n(.+?)\n", text)
                        nationality_judge_5= lines[35].strip()

                        """DUDAS"""

                        gender=gender_text.group(1) 
                        weight=weight_text.group(1)
                        referee=referee_text.group(1)
                        referee_nationality=referee_nationality_text.group(1)
                        judge_1=judge_1_text.group(1)
                        judge_2=judge_2_text.group(1)
                        judge_3=judge_3_text.group(1)
                        judge_4=judge_4_text.group(1)
                        judge_5=judge_5_text.group(1)
                        
                        # Update the dictionary with extracted values
                        Dictionary_boxing["gender"]=gender
                        Dictionary_boxing["weight"]=weight
                        Dictionary_boxing["phase of competition"]=phase

                        Dictionary_boxing["Name red boxer"]=red_boxer
                        Dictionary_boxing["Nationality red boxer"]=red_boxer_nationality

                        Dictionary_boxing["Name blue boxer"]=blue_boxer
                        Dictionary_boxing["Nationality blue boxer"]=blue_boxer_nationality

                        Dictionary_boxing["Winner"]=winner
                        Dictionary_boxing["Result"]=result
                        Dictionary_boxing["Decision"]=decision
        
                        Dictionary_boxing["Referee"]=referee
                        Dictionary_boxing["Referee nationality"]=referee_nationality

                        Dictionary_boxing["Judge 1"]=judge_1
                        Dictionary_boxing["Nationality Judge 1"]=nationality_judge_1

                        Dictionary_boxing["Judge 2"]=judge_2
                        Dictionary_boxing["Nationality Judge 2"]=nationality_judge_2

                        Dictionary_boxing["Judge 3"]=judge_3
                        Dictionary_boxing["Nationality Judge 3"]=nationality_judge_3

                        Dictionary_boxing["Judge 4"]=judge_4
                        Dictionary_boxing["Nationality Judge 4"]=nationality_judge_4

                        Dictionary_boxing["Judge 5"]=judge_5
                        Dictionary_boxing["Nationality Judge 5"]=nationality_judge_5

                        print(Dictionary_boxing)
                        
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
                        #print(f"Text from {number_of_match} - Page {page_num + 1}:{text}")
                        
                    pdf_document.close()  # Close the PDF file

                except Exception as e:

                    print(f"Error processing {number_of_match}: {e}")





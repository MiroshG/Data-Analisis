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

# DICTIONARIES ##

dictionary_persona={"name" :"",
                    "nationality":"",
                    "date birth":"",
                    "weight":"",
                    "gender":"",
                    "role":""}

dictionary_match={
                "Name red boxer":"",
                "Name blue boxer":"",
                "Referee":"",
                "Judge 1":"",
                "Judge 2":"",
                "Judge 3":"",
                "Judge 4":"",
                "Judge 5":"",
                "Winner":"",
                "Result":"",
                "Decision":""}

dictionary_points={
                "Judge":"",
                "Name red boxer":"",
                "Name blue boxer":"",
                "Boxer name points":"",
                "Round 1":"",
                "Round 2":"",
                "Round 3":"",
                "Total":""}

# LIST OF THE DICTIONARIES

list_persona=[]
list_match=[]
list_points=[]

# FUNCTIONS TO FILL THE DICTIONARIES

def fill_dictionary_persona(name, nationality, date_birth, weight, gender, role, dictionary):
    dictionary["name"]=name
    dictionary["nationality"]=nationality
    dictionary["date birth"]=date_birth
    dictionary["weight"]=weight
    dictionary["gender"]=gender
    dictionary["role"]=role

    list_persona.append(dictionary.copy())

def fill_dictionary_match(red_boxer, blue_boxer, referee, judge_1, judge_2, judge_3, judge_4, judge_5, winner_match, result, decision, dictionary):
    dictionary["Name red boxer"]=red_boxer
    dictionary["Name blue boxer"]=blue_boxer       
    dictionary["Referee"]=referee       
    dictionary["Judge 1"]=judge_1     
    dictionary["Judge 2"]=judge_2      
    dictionary["Judge 3"]=judge_3      
    dictionary["Judge 4"]=judge_4    
    dictionary["Judge 5"]=judge_5     
    dictionary["Winner"]=winner_match
    dictionary["Result"]=result
    dictionary["Decision"]=decision

    list_match.append(dictionary.copy())      

def fill_dictionary_points(judge, red_boxer, blue_boxer, boxer_name_points, round_1, round_2, round_3, total, dictionary):
    dictionary["Judge"]=judge
    dictionary["Name red boxer"]=red_boxer
    dictionary["Name blue boxer"]=blue_boxer
    dictionary["Boxer name points"]=boxer_name_points
    dictionary["Round 1"]=round_1
    dictionary["Round 2"]=round_2
    dictionary["Round 3"]=round_3
    dictionary["Total"]=total

    list_points.append(dictionary.copy())

# FUNCTION TO OBTAIN THE DATA FROM THE TABLE 
                

def points_judge(judge_index,tables):
    
    # JUST 1 ROUND #
    if len(tables[0])== 5: 
        round_1=0
        round_2=0
        round_3=0
        total=0

    # 2 ROUNDS #
    elif len(tables[0])== 5+1: 
        round_1=tables[0].iloc[3, judge_index+1]
        round_2=tables[0].iloc[4, judge_index+1]
        round_3=0
        total=tables[0].iloc[5, judge_index+1]

    # 3 ROUNDS #
    elif len(tables[0])== 5+2: 
        round_1=tables[0].iloc[3, judge_index+1]
        round_2=tables[0].iloc[4, judge_index+1]
        round_3=tables[0].iloc[5, judge_index+1]
        total=tables[0].iloc[6, judge_index+1]


    if isinstance(round_1, str):
        round_1_red , round_1_blue = round_1.split(" ")
    else:
        round_1_red , round_1_blue ="",""

    if isinstance(round_2, str):
        round_2_red , round_2_blue = round_2.split(" ")
    else:
        round_2_red , round_2_blue ="",""

    if isinstance(round_3, str):
        round_3_red , round_3_blue = round_3.split(" ")
    else:
        round_3_red , round_3_blue ="",""

    if isinstance(total, str):
        total_red , total_blue = total.split(" ")
    else:
        total_red , total_blue ="",""

    return(round_1_red , round_1_blue, round_2_red , round_2_blue, round_3_red , round_3_blue, total_red , total_blue)

def birth_year(boxer,text):
    match=re.search(rf"{re.escape(boxer)}\n(.+?)\n", text)
    date=match.group(1)
    year=date.split(" ")[-1]
    return(year)


    





############################################# LOOP TO RUN OVER ALL THE PDFS ##############################

pdf_start='C:\\Users\\Mirosh\\Desktop\\Data\\'
table_birth_year=""
tables=""

# List of weights to navigate through
#gender_boxers = ['H', 'M']
gender_boxers=['H2']

for gender in gender_boxers:

    gender_path = os.path.join(pdf_start, gender)
    weight_folders = os.listdir(gender_path)
    
    for weight in weight_folders:

        weight_path = os.path.join(gender_path, weight)
        boxing_folders = os.listdir(weight_path)  

        for boxing_phase in boxing_folders:  

            if boxing_phase=="Entry_list":

                file_path = os.path.join(weight_path, boxing_phase, "Entry_list.pdf")

                try:
                    pdf_document = fitz.open(file_path)
                    
                    # Process the PDF (e.g., extract text)
                    for page_num in range(pdf_document.page_count):

                        page = pdf_document.load_page(page_num)
                        text_dates = page.get_text("text")
                        lines=text_dates.split('\n')  # necessary to obtain some of the text
                        
                        #print(f"Text from {number_of_match} - Page {page_num + 1}:{text_dates}")

                        # REGULAR EXPRESSIONS IN THE FOLLOWING LINES: ################

                    pdf_document.close()  # Close the PDF file

                except Exception as e:

                    print(f"Error processing {number_of_match}: {e}")

            else:
                
                matches_path = os.path.join(weight_path, boxing_phase)
                list_matches=os.listdir(matches_path)

                for number_of_match in list_matches:


                    file_path = os.path.join(matches_path, number_of_match)


                    # Read tables from the PDF
                    tables = tabula.read_pdf(file_path, pages='all')

                    #print(len(tables[0]))
                    #print(tables)

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

                            if winner=="RED":
                                winner_match=red_boxer
                            elif winner=="BLUE":
                                winner_match=blue_boxer

                            result= lines[24].strip()
                            decision= lines[25].strip() 

                            referee_text= re.search(r"Referee:\n(.+?)\n", text)
                            referee_nationality_text=re.search(r"(.+)(?=\nJudge 1:)", text)

                            judge_1_text= re.search(r"Judge 1:\n(.+?)\n", text)
                            nationality_judge_1 = lines[27].strip()

                            judge_2_text= re.search(r"Judge 2:\n(.+?)\n", text)
                            nationality_judge_2 = lines[29].strip()

                            judge_3_text= re.search(r"Judge 3:\n(.+?)\n", text)
                            nationality_judge_3 = lines[31].strip()

                            judge_4_text= re.search(r"Judge 4:\n(.+?)\n", text)
                            nationality_judge_4 = lines[33].strip()

                            judge_5_text= re.search(r"Judge 5:\n(.+?)\n", text)
                            nationality_judge_5 = lines[35].strip()

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

                        pdf_document.close()  # Close the PDF file

                    except Exception as e:

                        print(f"Error processing {number_of_match}: {e}")
                            
                    
                    # UPDATE THE DICTIONARY PERSONA #####################################################

                    name_list=[red_boxer, blue_boxer, referee, judge_1, judge_2, judge_3, judge_4, judge_5]
                    nationality_list=[red_boxer_nationality, blue_boxer_nationality, referee_nationality, nationality_judge_1, nationality_judge_2, nationality_judge_3, nationality_judge_4, nationality_judge_5]

                    red_boxer_year=birth_year(red_boxer, text_dates)
                    blue_boxer_year=birth_year(blue_boxer, text_dates)

                    date_birth_list=[red_boxer_year, blue_boxer_year, "", "", "", "", "", ""]
                    weight_list=[weight, weight, "", "", "", "", "", ""]
                    gender_list=[gender, gender, "", "", "", "", "", ""]
                    role_list=["boxer", "boxer", "referee", "judge", "judge", "judge", "judge", "judge"]

                    for i in range(len(name_list)):
                        fill_dictionary_persona(name_list[i], nationality_list[i], date_birth_list[i], weight_list[i], gender_list[i], role_list[i], dictionary_persona)

                    # UPDATE THE DICTIONARY MATCH #######################################################

                    fill_dictionary_match(red_boxer, blue_boxer, referee, judge_1, judge_2, judge_3, judge_4, judge_5, winner_match, result, decision, dictionary_match)

                    # UPDATE THE DICTIONARY POINTS #######################################################

                    judges_list=[judge_1, judge_2, judge_3, judge_4, judge_5]

                    for i in range(len(judges_list)):

                        round_1_red , round_1_blue, round_2_red , round_2_blue, round_3_red , round_3_blue, total_red , total_blue=points_judge(i, tables)

                        fill_dictionary_points(judges_list[i], red_boxer, blue_boxer, red_boxer, round_1_red, round_2_red, round_3_red, total_red, dictionary_points) # red boxer

                        fill_dictionary_points(judges_list[i], red_boxer, blue_boxer, blue_boxer, round_1_blue, round_2_blue, round_3_blue, total_blue, dictionary_points) # blue boxer

            
print(list_match)




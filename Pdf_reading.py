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

cursor = conn.cursor()

# DICTIONARIES ##

dictionary_persona={"name" :"",
                    "nationality":"",
                    "birth_date":"",
                    "weight":"",
                    "gender":"",
                    "role":""}

dictionary_match={
                "phase":"",
                "id_boxer_red":"",
                "id_boxer_blue":"",
                "id_referee":"",
                "id_judge_1":"",
                "id_judge_2":"",
                "id_judge_3":"",
                "id_judge_4":"",
                "id_judge_5":"",
                "id_winner":"",
                "result":"",
                "decision":""}

dictionary_points={
                "id_judge":"",
                "name_boxer_red":"",
                "name_boxer_blue":"",
                "id_boxer":"",
                "points_1":"",
                "points_2":"",
                "points_3":"",
                "total":""}

# LIST OF THE DICTIONARIES

list_persona=[]
list_match=[]
list_points=[]

# FUNCTIONS TO FILL THE DICTIONARIES

def fill_dictionary_persona(name, nationality, birth_date, weight, gender, role, dictionary):
    dictionary["name"]=name
    dictionary["nationality"]=nationality
    dictionary["birth_date"]=birth_date
    dictionary["weight"]=weight
    dictionary["gender"]=gender
    dictionary["role"]=role
    exist=False
    
    for dict in list_persona:
        if dict['name']== name and dict['weight']== weight and dict['role']==role: # and (dict['role']=='judge' or dict['role']=='referee'):
            exist=True

    if exist==False:
        list_persona.append(dictionary.copy())


def fill_dictionary_match(phase, red_boxer, blue_boxer, referee, judge_1, judge_2, judge_3, judge_4, judge_5, winner_match, result, decision, dictionary):
    dictionary["phase"]=phase
    dictionary["id_boxer_red"]=red_boxer
    dictionary["id_boxer_blue"]=blue_boxer       
    dictionary["id_referee"]=referee       
    dictionary["id_judge_1"]=judge_1     
    dictionary["id_judge_2"]=judge_2      
    dictionary["id_judge_3"]=judge_3      
    dictionary["id_judge_4"]=judge_4    
    dictionary["id_judge_5"]=judge_5     
    dictionary["id_winner"]=winner_match
    dictionary["result"]=result
    dictionary["decision"]=decision

    list_match.append(dictionary.copy())      

def fill_dictionary_points(judge, red_boxer, blue_boxer, boxer_name_points, round_1, round_2, round_3, total, dictionary):
    dictionary["id_judge"]=judge
    dictionary["name_boxer_red"]=red_boxer
    dictionary["name_boxer_blue"]=blue_boxer
    dictionary["id_boxer"]=boxer_name_points
    dictionary["points_1"]=round_1
    dictionary["points_2"]=round_2
    dictionary["points_3"]=round_3
    dictionary["total"]=total

    list_points.append(dictionary.copy())

# FUNCTION TO OBTAIN THE DATA FROM THE TABLE 
                

def points_judge(judge_index,tables):
    
    # JUST 1 ROUND #

    try:
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

        try:
            if isinstance(round_1, str):
                round_1_red , round_1_blue = round_1.split(" ")
                round_1_red=int(round_1_red)
                round_1_blue=int(round_1_blue)

            else:
                round_1_red , round_1_blue =None, None

            if isinstance(round_2, str):
                round_2_red , round_2_blue = round_2.split(" ")
                round_2_red=int(round_2_red)
                round_2_blue=int(round_2_blue)
            else:
                round_2_red , round_2_blue =None, None

            if isinstance(round_3, str):
                round_3_red , round_3_blue = round_3.split(" ")
                round_3_red=int(round_3_red)
                round_3_blue=int(round_3_blue)
            else:
                round_3_red , round_3_blue =None, None

            if isinstance(total, str):
                total_red , total_blue = total.split(" ")
                total_red=int(total_red)
                total_blue=int(total_blue)
            else:
                total_red , total_blue =None, None
        
            return(round_1_red , round_1_blue, round_2_red , round_2_blue, round_3_red , round_3_blue, total_red , total_blue)
        except UnboundLocalError:
            return(None, None, None, None, None, None, None,None)
    except IndexError:
        return(None, None, None, None, None, None, None,None)


def birth_year(boxer,text):
    surname=boxer.split(" ")[0]
    name=boxer.split(" ")[1]
    find_boxer=surname+" "+name
    if name.isupper():
        find_boxer=surname
    match=re.search(rf"{re.escape(find_boxer)}\s+(.*?)\n(.+?)\n", text)
    number_of_names=boxer.count(' ')
    if number_of_names>=2:
        date=match.group(2)
    else:
        date=match.group(1)
    year=date.split(" ")[-1]
    return(int(year))

def weight_092(boxer,text):
    lines = text.split("\n")

    j = None
    for i, line in enumerate(lines):
        if re.search(re.escape(boxer), line):
            j = i  
            break

    weight_to_obtain=lines[j+2].strip()
    kg=weight_to_obtain.split()[0]
    """boxer_weight=re.search(rf"({re.escape(boxer)}.*(?:\n.+)+)", text)
    weight_to_obtain=boxer_weight.group(1)
    kg=weight_to_obtain.split('\\')[1]"""
    return(float(kg))

def open_and_read_file_Entry_list(file_path):
    try:
        pdf_document = fitz.open(file_path)
        
        
        for page_num in range(pdf_document.page_count):

            page = pdf_document.load_page(page_num)
            text_dates = page.get_text("text")
            

            # REGULAR EXPRESSIONS IN THE FOLLOWING LINES: ################

        pdf_document.close()  # Close the PDF file
        return(text_dates)

    except Exception as e:

        print(f"Error processing {file_path}: {e}")
    
    

    





############################################# LOOP TO RUN OVER ALL THE PDFS ##############################

pdf_start='C:\\Users\\Mirosh\\Desktop\\Data\\'

# List of weights to navigate through
gender_boxers = ['H','M']
#gender_boxers=['H2']

for gender in gender_boxers:

    gender_path = os.path.join(pdf_start, gender)
    weight_folders = os.listdir(gender_path)
    
    for weight in weight_folders:

        weight_path = os.path.join(gender_path, weight)
        boxing_folders = os.listdir(weight_path)  

        for boxing_phase in boxing_folders:  

            if boxing_phase=="Entry_list":

                file_path = os.path.join(weight_path, boxing_phase, "Entry_list.pdf")

                text_dates=open_and_read_file_Entry_list(file_path)

                


                if weight=='O92':
                    
                    file_path_2 = os.path.join(weight_path, boxing_phase, "Entry_list_weight.pdf")

                    text_weight=open_and_read_file_Entry_list(file_path_2)
                    
            else:
                
                matches_path = os.path.join(weight_path, boxing_phase)
                list_matches=os.listdir(matches_path)

                for number_of_match in list_matches:


                    file_path = os.path.join(matches_path, number_of_match)


                    # Read tables from the PDF
                    tables = tabula.read_pdf(file_path, pages='all')


                    ##################################################################################################################
                    ##############################         DATA OF THE PARTICIPANTS OF THE MATCH         #############################
                    ##################################################################################################################


                    try:
                        pdf_document = fitz.open(file_path)
                        print(file_path)
                        
                        for page_num in range(pdf_document.page_count):

                            page = pdf_document.load_page(page_num)
                            text = page.get_text("text")
                            lines=text.split('\n')  # necessary to obtain some of the text
                            

                            # REGULAR EXPRESSIONS IN THE FOLLOWING LINES: ################
                            

                            gender_text= re.search(r"(MEN|WOMEN)'S", text)
                            

                            red_boxer= lines[19].strip()
                            red_boxer_nationality=lines[20].strip()

                            blue_boxer= lines[21].strip()
                            blue_boxer_nationality=lines[22].strip()

                            if weight=='O92':
                                weight_of_boxer_blue=weight_092(blue_boxer,text_weight)
                                weight_of_boxer_red=weight_092(red_boxer,text_weight)
                                weight_list=[weight_of_boxer_red, weight_of_boxer_blue, None, None, None, None, None, None]
                            else:
                                weight_list=[float(weight), float(weight), None, None, None, None, None, None]

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

                            gender=gender_text.group(1) 
                            referee=referee_text.group(1)
                            referee_nationality=referee_nationality_text.group(1)
                            judge_1=judge_1_text.group(1)
                            judge_2=judge_2_text.group(1)
                            judge_3=judge_3_text.group(1)
                            judge_4=judge_4_text.group(1)
                            judge_5=judge_5_text.group(1)

                        pdf_document.close()  

                    except Exception as e:

                        print(f"Error processing {number_of_match}: {e}")
                            
                    
                    # UPDATE THE DICTIONARY PERSONA #####################################################

                    name_list=[red_boxer, blue_boxer, referee, judge_1, judge_2, judge_3, judge_4, judge_5]
                    nationality_list=[red_boxer_nationality, blue_boxer_nationality, referee_nationality, nationality_judge_1, nationality_judge_2, nationality_judge_3, nationality_judge_4, nationality_judge_5]

                    
                    red_boxer_year=birth_year(red_boxer, text_dates)
                    blue_boxer_year=birth_year(blue_boxer, text_dates)

                    date_birth_list=[red_boxer_year, blue_boxer_year, None, None, None, None, None, None]
                    gender_list=[gender, gender, "", "", "", "", "", ""]
                    role_list=["boxer", "boxer", "referee", "judge", "judge", "judge", "judge", "judge"]

                    for i in range(len(name_list)):
                        fill_dictionary_persona(name_list[i], nationality_list[i], date_birth_list[i], weight_list[i], gender_list[i], role_list[i], dictionary_persona)

                    # UPDATE THE DICTIONARY MATCH #######################################################

                    fill_dictionary_match(boxing_phase, red_boxer, blue_boxer, referee, judge_1, judge_2, judge_3, judge_4, judge_5, winner_match, result, decision, dictionary_match)

                    # UPDATE THE DICTIONARY POINTS #######################################################

                    judges_list=[judge_1, judge_2, judge_3, judge_4, judge_5]

                    for i in range(len(judges_list)):

                        round_1_red , round_1_blue, round_2_red , round_2_blue, round_3_red , round_3_blue, total_red , total_blue=points_judge(i, tables)

                        fill_dictionary_points(judges_list[i], red_boxer, blue_boxer, red_boxer, round_1_red, round_2_red, round_3_red, total_red, dictionary_points) # red boxer

                        fill_dictionary_points(judges_list[i], red_boxer, blue_boxer, blue_boxer, round_1_blue, round_2_blue, round_3_blue, total_blue, dictionary_points) # blue boxer




cursor.executemany("""
    INSERT INTO persona (name,nationality,birth_date,weight,gender,role)
    VALUES (%(name)s, %(nationality)s, %(birth_date)s, %(weight)s, %(gender)s, %(role)s)""", list_persona)
conn.commit()       

list_names=[]
for dictionary in list_match:
    list_names.append(dictionary["id_boxer_red"])
    list_names.append(dictionary["id_boxer_blue"])
    list_names.append(dictionary["id_referee"])
    list_names.append(dictionary["id_judge_1"])
    list_names.append(dictionary["id_judge_2"])
    list_names.append(dictionary["id_judge_3"])
    list_names.append(dictionary["id_judge_4"])
    list_names.append(dictionary["id_judge_5"])

parsed_names = ",".join(list_names)  #parsed_names="name1,name2,name3,..."
format_strings = ','.join(['%s'] * len(list_names)) #format_string="%s %s,%s,...""

query_names = "select id, name from persona where name in( " + format_strings+")" # query to obtain the list of names
cursor.execute(query_names,list_names) 

result_names=cursor.fetchall() # gives me id and name

for dictionary in list_match:        
    name_boxer_red = dictionary["id_boxer_red"] # get the name 
    id_boxer_red =[row[0] for row in result_names if row[1] == name_boxer_red][0] # compare the name with the list 
    dictionary["id_boxer_red"]=id_boxer_red                                 # result_names and takes the id corresponding 
    name_boxer_blue = dictionary["id_boxer_blue"]                           # to that name
    id_boxer_blue =[row[0] for row in result_names if row[1] == name_boxer_blue][0]
    dictionary["id_boxer_blue"]=id_boxer_blue
    name_referee = dictionary["id_referee"]
    id_referee =[row[0] for row in result_names if row[1] == name_referee][0]
    dictionary["id_referee"]=id_referee
    name_judge_1 = dictionary["id_judge_1"]
    id_judge_1 =[row[0] for row in result_names if row[1] == name_judge_1][0]
    dictionary["id_judge_1"]=id_judge_1
    name_judge_2 = dictionary["id_judge_2"]
    id_judge_2 =[row[0] for row in result_names if row[1] == name_judge_2][0]
    dictionary["id_judge_2"]=id_judge_2
    name_judge_3 = dictionary["id_judge_3"]
    id_judge_3 =[row[0] for row in result_names if row[1] == name_judge_3][0]
    dictionary["id_judge_3"]=id_judge_3
    name_judge_4 = dictionary["id_judge_4"]
    id_judge_4 =[row[0] for row in result_names if row[1] == name_judge_4][0]
    dictionary["id_judge_4"]=id_judge_4
    name_judge_5 = dictionary["id_judge_5"]
    id_judge_5 =[row[0] for row in result_names if row[1] == name_judge_5][0]
    dictionary["id_judge_5"]=id_judge_5
    name_winner = dictionary["id_winner"]
    id_winner =[row[0] for row in result_names if row[1] == name_winner][0]
    dictionary["id_winner"]=id_winner

cursor.executemany("""
    INSERT INTO matches (phase,id_boxer_red,id_boxer_blue,id_referee,id_judge_1,id_judge_2,id_judge_3,id_judge_4,id_judge_5,id_winner,result,decision)
    VALUES (%(phase)s, %(id_boxer_red)s, %(id_boxer_blue)s, 
    %(id_referee)s, %(id_judge_1)s, %(id_judge_2)s,
    %(id_judge_3)s, %(id_judge_4)s, 
    %(id_judge_5)s, %(id_winner)s, %(result)s, %(decision)s)""", list_match)
conn.commit()       


list_name_ids = [row[0] for row in result_names]
format_strings = ','.join(['%s'] * len(result_names)) #format_string="%s %s,%s,...""

# query to obtain the list of matches
query_matches = "select id, id_boxer_red, id_boxer_blue from matches where id_boxer_red in( " + format_strings+") or id_boxer_blue in ( " + format_strings+")" 
cursor.execute(query_matches,list_name_ids+ list_name_ids) # list_names_ids twice to give the names for red and for blue

result_matches=cursor.fetchall() # gives me id of the match, id boxer red, id boxer blue

for dictionary in list_points:        
    name_boxer_red = dictionary["name_boxer_red"]
    id_boxer_red = [row[0] for row in result_names if row[1] == name_boxer_red][0]
    name_boxer_blue = dictionary["name_boxer_blue"]
    id_boxer_blue = [row[0] for row in result_names if row[1] == name_boxer_blue][0]
    id_match=[row[0] for row in result_matches if row[1] == id_boxer_red and row[2] == id_boxer_blue][0]
    dictionary["id_match"]=id_match # add new key
    dictionary.pop("name_boxer_red")  # remove the old ones
    dictionary.pop("name_boxer_blue")
    name_boxer = dictionary["id_boxer"]
    id_boxer =[row[0] for row in result_names if row[1] == name_boxer][0]
    dictionary["id_boxer"]=id_boxer
    name_judge = dictionary["id_judge"]
    id_judge =[row[0] for row in result_names if row[1] == name_judge][0]
    dictionary["id_judge"]=id_judge


cursor.executemany("""
    INSERT INTO points (id_judge,id_match,id_boxer,points_1,points_2,points_3,total)
    VALUES (%(id_judge)s, %(id_match)s,%(id_boxer)s, %(points_1)s, %(points_2)s, %(points_3)s, %(total)s)""", list_points)
conn.commit()  

cursor.close()
conn.close()


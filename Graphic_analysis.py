import mysql.connector
import matplotlib.pyplot as plt


conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345'
)

cursor = conn.cursor()

cursor.execute("select * from boxing_data.persona")

results_persona = cursor.fetchall()

cursor.execute("select * from boxing_data.matches")

results_matches = cursor.fetchall()

conn.close()

conn_panam = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='boxing_data_panamerican'
)

cursor_panam = conn_panam.cursor()

cursor_panam.execute("select * from boxing_data_panamerican.persona")

results_persona_panam = cursor_panam.fetchall()

cursor_panam.execute("select * from boxing_data_panamerican.matches")

results_matches_panam = cursor_panam.fetchall()

cursor_panam.execute("select * from boxing_data_panamerican.points")

results_points_panam= cursor_panam.fetchall()

conn_panam.close()

##############################################  NATIONALITIES ########################################################################

def nationality_boxer_histogram():
    nationality_dictionary={}

    for row in results_persona:
        if row[-1] == 'boxer':
            if row[2] in nationality_dictionary:
                nationality_dictionary[row[2]] +=1
            else:
                nationality_dictionary[row[2]]= 1

    nationality_list=list(nationality_dictionary.keys())
    population_list=list(nationality_dictionary.values())   

    total=sum(population_list)

    normalized_nat_list=[x*100/total for x in population_list]

    plt.figure(figsize=(8, 6))
    plt.bar(nationality_list, normalized_nat_list, color='skyblue')
    plt.xlabel('Nationalities')
    plt.ylabel('Percentage of boxers (%)')
    plt.xticks(rotation=45, fontsize=8) 
    plt.tight_layout()
    #plt.show()
    plt.savefig('percentage_nationalities.png', dpi=300, bbox_inches='tight')

nationality_boxer_histogram()
    
def nationality_boxer_histogram_panam():
    nationality_dictionary={}

    for row in results_persona_panam:
        if row[-1] == 'boxer':
            if row[2] in nationality_dictionary:
                nationality_dictionary[row[2]] +=1
            else:
                nationality_dictionary[row[2]]= 1

    nationality_list=list(nationality_dictionary.keys())
    population_list=list(nationality_dictionary.values())   

    total=sum(population_list)

    normalized_nat_list=[x*100/total for x in population_list]

    plt.figure(figsize=(8, 6))
    plt.bar(nationality_list, normalized_nat_list, color='darkcyan')
    plt.xlabel('Nationalities')
    plt.ylabel('Percentage of boxers (%)')
    plt.xticks(rotation=45, fontsize=8) 
    plt.tight_layout()
    #plt.show()
    plt.savefig('percentage_nationalities_panam.png', dpi=300, bbox_inches='tight')

nationality_boxer_histogram_panam()

def nationality_judge_histogram():
    nationality_judge_dictionary={}

    for row in results_persona:
        if row[-1] == 'judge':
            if row[2] in nationality_judge_dictionary:
                nationality_judge_dictionary[row[2]] +=1
            else:
                nationality_judge_dictionary[row[2]]= 1


    nationality_list=list(nationality_judge_dictionary.keys())
    population_list=list(nationality_judge_dictionary.values())   

    total=sum(population_list)

    normalized_nat_list=[x*100/total for x in population_list]

    plt.figure(figsize=(8, 6))
    plt.bar(nationality_list, normalized_nat_list, color='orange')
    plt.xlabel('Nationalities')
    plt.ylabel('Percentage of judges (%)')
    plt.xticks(rotation=45, fontsize=8) 
    plt.tight_layout()
    #plt.show()
    plt.savefig('percentage_nationalities_judge.png', dpi=300, bbox_inches='tight')

nationality_judge_histogram()

def nationality_judge_histogram_panam():
    nationality_judge_dictionary_panam={}

    for row in results_persona_panam:
        if row[-1] == 'judge':
            if row[2] in nationality_judge_dictionary_panam:
                nationality_judge_dictionary_panam[row[2]] +=1
            else:
                nationality_judge_dictionary_panam[row[2]]= 1


    nationality_list_panam=list(nationality_judge_dictionary_panam.keys())
    population_list_panam=list(nationality_judge_dictionary_panam.values())   

    total=sum(population_list_panam)

    normalized_nat_list=[x*100/total for x in population_list_panam]

    plt.figure(figsize=(8, 6))
    plt.bar(nationality_list_panam, normalized_nat_list, color='darkblue')
    plt.xlabel('Nationalities')
    plt.ylabel('Percentage of judges (%)')
    plt.xticks(rotation=45, fontsize=8) 
    plt.tight_layout()
    #plt.show()
    plt.savefig('percentage_nationalities_judge_panam.png', dpi=300, bbox_inches='tight')

nationality_judge_histogram_panam()


##############################################  VICTORIES  ########################################################################

def victories_histogram():

    victories_dictionary={}
    number_of_fights_dictionary={}
    nationality_dictionary={}

    for row_persona in results_persona:
        if row_persona[-1] == 'boxer':
            if row_persona[2] in nationality_dictionary:
                nationality_dictionary[row_persona[2]] +=1
            else:
                nationality_dictionary[row_persona[2]]= 1
            boxer=row_persona[0]
            nationality=row_persona[2]

            for row_matches in results_matches:
                if row_matches[2]==boxer or row_matches[3]==boxer:

                    if nationality in number_of_fights_dictionary:
                        number_of_fights_dictionary[nationality]+=1
                    else:
                        number_of_fights_dictionary[nationality]=1

                if row_matches[10]==boxer:
                    if nationality in victories_dictionary:
                        victories_dictionary[nationality] +=1
                    else:
                        victories_dictionary[nationality] =1
    

    for nationality in victories_dictionary:
        if nationality in number_of_fights_dictionary:  
            nationality_dictionary[nationality] = victories_dictionary[nationality]*100 / number_of_fights_dictionary[nationality]

    year_list=list(nationality_dictionary.keys())
    normalized_fights_list=list(nationality_dictionary.values())


   


    plt.figure(figsize=(8, 6))
    plt.bar(year_list, normalized_fights_list, color='red')
    plt.xlabel('Nationalities')
    plt.ylabel('Percentage of wins for each nationality(%)')
    plt.xticks(year_list, rotation=45, fontsize=8) 
    plt.tight_layout()
    #plt.show()
    plt.savefig('percentage_victories.png', dpi=300, bbox_inches='tight')

victories_histogram()

def victories_histogram_panam():

    victories_dictionary={}
    number_of_fights_dictionary={}
    nationality_dictionary={}

    for row_persona in results_persona_panam:
        if row_persona[-1] == 'boxer':
            if row_persona[2] in nationality_dictionary:
                nationality_dictionary[row_persona[2]] +=1
            else:
                nationality_dictionary[row_persona[2]]= 1
            boxer=row_persona[0]
            nationality=row_persona[2]

            for row_matches in results_matches_panam:
                if row_matches[2]==boxer or row_matches[3]==boxer:

                    if nationality in number_of_fights_dictionary:
                        number_of_fights_dictionary[nationality]+=1
                    else:
                        number_of_fights_dictionary[nationality]=1

                if row_matches[10]==boxer:
                    if nationality in victories_dictionary:
                        victories_dictionary[nationality] +=1
                    else:
                        victories_dictionary[nationality] =1
    

    for nationality in victories_dictionary:
        if nationality in number_of_fights_dictionary:  
            nationality_dictionary[nationality] = victories_dictionary[nationality]*100 / number_of_fights_dictionary[nationality]

    year_list=list(nationality_dictionary.keys())
    normalized_fights_list=list(nationality_dictionary.values())


   


    plt.figure(figsize=(8, 6))
    plt.bar(year_list, normalized_fights_list, color='green')
    plt.xlabel('Nationalities')
    plt.ylabel('Percentage of wins for each nationality(%)')
    plt.xticks(year_list, rotation=45, fontsize=8) 
    plt.tight_layout()
    #plt.show()
    plt.savefig('percentage_victories_panam.png', dpi=300, bbox_inches='tight')

victories_histogram_panam()



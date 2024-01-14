import mysql.connector
import matplotlib.pyplot as plt


conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='boxing_data'
)

cursor = conn.cursor()

cursor.execute("select * from boxing_data.persona")

results_nationality = cursor.fetchall()

cursor.execute("select * from boxing_data.matches")

results_victory = cursor.fetchall()

# Close the connection
conn.close()

##############################################  NATIONALITIES ########################################################################

def nationality_boxer_histogram():
    nationality_dictionary={}

    for row in results_nationality:
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

#nationality_boxer_histogram()

def nationality_judge_histogram():
    nationality_judge_dictionary={}

    for row in results_nationality:
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
    plt.bar(nationality_list, normalized_nat_list, color='skyblue')
    plt.xlabel('Nationalities')
    plt.ylabel('Percentage of judges (%)')
    plt.xticks(rotation=45, fontsize=8) 
    plt.tight_layout()
    #plt.show()
    plt.savefig('percentage_nationalities_judge.png', dpi=300, bbox_inches='tight')

nationality_judge_histogram()


##############################################  VICTORIES  ########################################################################

def victories_histogram():

    victories_dictionary={}
    number_of_fights_dictionary={}

    for row_persona in results_nationality:
        if row_persona[-1] == 'boxer':
            boxer=row_persona[0]
            year=row_persona[3]

            for row_matches in results_victory:
                if row_matches[2]==boxer or row_matches[3]==boxer:

                    if year in number_of_fights_dictionary:
                        number_of_fights_dictionary[year]+=1
                    else:
                        number_of_fights_dictionary[year]=1

                if row_matches[10]==boxer:
                    if year in victories_dictionary:
                        victories_dictionary[year] +=1
                    else:
                        victories_dictionary[year] =1
    

    normalized_dictionary = {}
    for year in victories_dictionary:
        if year in number_of_fights_dictionary:  
            normalized_dictionary[year] = victories_dictionary[year]*100 / number_of_fights_dictionary[year]

    year_list=list(normalized_dictionary.keys())
    normalized_fights_list=list(normalized_dictionary.values())


   


    plt.figure(figsize=(8, 6))
    plt.bar(year_list, normalized_fights_list, color='skyblue')
    plt.xlabel('Year of birth')
    plt.ylabel('Percentage of wins (%)')
    plt.xticks(year_list, rotation=45, fontsize=8) 
    plt.tight_layout()
    #plt.show()
    plt.savefig('percentage_victories.png', dpi=300, bbox_inches='tight')

victories_histogram()


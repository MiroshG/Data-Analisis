import mysql.connector
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from scipy.stats import chisquare
import scipy as sp
from scipy.optimize import curve_fit
from scipy.stats import linregress

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

conn_panam.close()

def percentages_function():

    nationality_dictionary={}
    all_nationalities_dictionary={}

    for row in results_persona:
        if row[-1] == 'boxer':
            if row[2] in nationality_dictionary:
                nationality_dictionary[row[2]] +=1
            else:
                nationality_dictionary[row[2]]= 1
                all_nationalities_dictionary[row[2]]=0

    nationality_list=list(nationality_dictionary.keys())
    population_list=list(nationality_dictionary.values())   

    total=sum(population_list)

    normalized_nat_list=[x*100/total for x in population_list] # percentage of boxers from EU

    nationality_dictionary_panam={}

    for row in results_persona_panam:
        if row[-1] == 'boxer':
            if row[2] in nationality_dictionary_panam:
                nationality_dictionary_panam[row[2]] +=1
            else:
                nationality_dictionary_panam[row[2]]= 1
                all_nationalities_dictionary[row[2]]=0

    nationality_list_panam=list(nationality_dictionary_panam.keys())
    population_list_panam=list(nationality_dictionary_panam.values())   

    total=sum(population_list_panam)

    normalized_nat_list_panam=[x*100/total for x in population_list_panam] # percentage of boxers from PANAM

    victories_dictionary={}
    number_of_fights_dictionary={}
    nationality_dictionary_wins={}

    for row_persona in results_persona:
        if row_persona[-1] == 'boxer':
            if row_persona[2] in nationality_dictionary_wins:
                nationality_dictionary_wins[row_persona[2]] +=1
            else:
                nationality_dictionary_wins[row_persona[2]]= 1
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

    # Percentage of wins by each nationality EU
    for nationality in victories_dictionary:
        if nationality in number_of_fights_dictionary:  
            nationality_dictionary_wins[nationality] = victories_dictionary[nationality]*100 / number_of_fights_dictionary[nationality]

    percentage_wins=list(nationality_dictionary_wins.values())  


    victories_dictionary_panam={}
    number_of_fights_dictionary_panam={}
    nationality_dictionary_wins_panam={}

    for row_persona in results_persona_panam:
        if row_persona[-1] == 'boxer':
            if row_persona[2] in nationality_dictionary_wins_panam:
                nationality_dictionary_wins_panam[row_persona[2]] +=1
            else:
                nationality_dictionary_wins_panam[row_persona[2]]= 1
            boxer=row_persona[0]
            nationality=row_persona[2]

            for row_matches in results_matches_panam:
                if row_matches[2]==boxer or row_matches[3]==boxer:

                    if nationality in number_of_fights_dictionary_panam:
                        number_of_fights_dictionary_panam[nationality]+=1
                    else:
                        number_of_fights_dictionary_panam[nationality]=1

                if row_matches[10]==boxer:
                    if nationality in victories_dictionary_panam:
                        victories_dictionary_panam[nationality] +=1
                    else:
                        victories_dictionary_panam[nationality] =1
    

    for nationality in victories_dictionary_panam:
        if nationality in number_of_fights_dictionary_panam:  
            nationality_dictionary_wins_panam[nationality] = victories_dictionary_panam[nationality]*100 / number_of_fights_dictionary_panam[nationality]

    percentage_wins_panam=list(nationality_dictionary_wins_panam.values())

    #percentage of boxers in the tournament
    normalized_nat_list=normalized_nat_list +normalized_nat_list_panam
    #percentage of boxers wins in the tournament
    percentage_wins=percentage_wins+percentage_wins_panam

    slope, intercept, r_value, p_value, _ = linregress(normalized_nat_list, percentage_wins)

    correlation_coefficient = np.corrcoef(normalized_nat_list, percentage_wins)[0, 1]
    normalized_nat_list=np.array(normalized_nat_list)

    y_teor=slope * normalized_nat_list + intercept

    plt.figure()
    plt.scatter(normalized_nat_list, percentage_wins)
    plt.plot(normalized_nat_list,y_teor, color='red', label=f'r={r_value:2f}, p-value={p_value}')
    plt.xlabel('Percentage of boxers (%)')
    plt.ylabel('Percentage of wins(%)')
    plt.legend()
    plt.savefig('Percentage.png')
    

    

percentages_function()

    
    
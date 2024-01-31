import mysql.connector
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from scipy.stats import chisquare
import scipy as sp
from scipy.optimize import curve_fit
import re

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='boxing_data'
)

cursor = conn.cursor()

cursor.execute("select * from boxing_data.persona")

results_persona = cursor.fetchall()

cursor.execute("select * from boxing_data.matches")

results_matches = cursor.fetchall()

cursor.execute("select * from boxing_data.points")

results_points= cursor.fetchall()

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

def logistic_function(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))

def prob_winning_men():

    points_difference_dict={}  # dictionary with the points in each match
    win_or_lose_binary_dict={} # dict to save if the red boxer wins (1) or loses (0) in each match

    for row_matches in results_matches:
        id_match=row_matches[0]
        id_winner=row_matches[10]
        id_boxer_red=row_matches[2]
        id_boxer_blue=row_matches[3]

        for row_persona in results_persona:
            if row_persona[0]==id_boxer_red:
                gender=row_persona[5]
                if gender=='MEN':

                    first_and_second_points=0       # restart for every new match
                    
                    for row_points in results_points:
                        if row_points[2]==id_match and row_points[5]!=0 and row_points[5]!= None: # condition that the fight had 3 rounds

                            if id_winner==id_boxer_red:
                                win_or_lose_binary_dict[id_match]=1 
                            else:
                                win_or_lose_binary_dict[id_match]=0
                            
                            if row_points[3]==id_boxer_red:  # add points for the red boxer
                                first_and_second_points += row_points[4]
                                first_and_second_points += row_points[5]
                            
                            if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                first_and_second_points -= row_points[4]
                                first_and_second_points -= row_points[5]

                            points_difference_dict[id_match]=first_and_second_points  

    

    for row_matches in results_matches_panam:
        id_match=row_matches[0]
        id_winner=row_matches[10]
        id_boxer_red=row_matches[2]
        id_boxer_blue=row_matches[3]

        for row_persona in results_persona_panam:
            if row_persona[0]==id_boxer_red:
                gender=row_persona[5]
                if gender=='Men':

                    first_and_second_points=0       # restart for every new match
                    
                    for row_points in results_points_panam:
                        if row_points[2]==id_match and row_points[5]!=None: # condition that the fight had 3 rounds

                            if id_winner==id_boxer_red:
                                win_or_lose_binary_dict[id_match]=1 
                            else:
                                win_or_lose_binary_dict[id_match]=0
                            
                            if row_points[3]==id_boxer_red:  # add points for the red boxer
                                first_and_second_points += row_points[4]
                                first_and_second_points += row_points[5]
                            
                            if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                first_and_second_points -= row_points[4]
                                first_and_second_points -= row_points[5]

                            points_difference_dict[id_match]=first_and_second_points 

    
    win_or_lose_list=list(win_or_lose_binary_dict.values())          # list with the result of each of these matches
    points_difference_list=list(points_difference_dict.values())     # list with the difference in point of each of these matches

    element_counts = Counter(points_difference_list)
    different_results_dict = dict(element_counts)  # dictionary with the different in points and the number of times this different happens

    sorted_keys = sorted(different_results_dict.keys())
    rearranged_different_results_dict = {key: different_results_dict[key] for key in sorted_keys}

    different_results_list=list(different_results_dict.keys()) 

    rearranged_different_results_list=list(rearranged_different_results_dict.keys()) 
    rearranged_different_results_values_list=list(rearranged_different_results_dict.values()) 


    positions_dict = {}

    # Loop through the list and populate the dictionary
    for index, value in enumerate(points_difference_list):
        if value not in positions_dict:
            positions_dict[value] = [index]
        else:
            positions_dict[value].append(index)

    

    mean_dict = {key: np.mean([win_or_lose_list[i] for i in indices]) for key, indices in positions_dict.items()}

    """print('mean_dict')
    print(mean_dict)
    print('win_or_lose_list')
    print(win_or_lose_list)
    print('points_difference_list')
    print(points_difference_list)
    print('positions_dict')
    print(positions_dict)
    print('different_results_list')
    print(different_results_list)"""

    points_difference_mean_list=list(mean_dict.values())   

    popt, pcov = curve_fit(logistic_function, different_results_list, points_difference_mean_list, bounds=([0, 0, 0], [1, 1, 10]))

    x_fit = np.linspace(min(different_results_list), max(different_results_list), 100)
    y_fit = logistic_function(x_fit, *popt)

    print('PARAMETERS MEN:')
    print(popt)
    print('ERRORS MEN')
    print(pcov)

    plt.figure()
    plt.scatter(different_results_list, points_difference_mean_list, label='')
    plt.plot(x_fit, y_fit, label='Logistic Fit', color='orange')
    plt.xlabel('Points difference in the first two rounds')
    plt.ylabel('Probability of winning')
    plt.title('MEN SAMPLE')
    plt.legend()
    plt.grid(False)
    #plt.show()
    plt.savefig('Men sample.png', dpi=300, bbox_inches='tight')

    return(rearranged_different_results_dict)

#rearranged_different_results_men_dict=prob_winning_men()

def prob_winning_women():

    points_difference_dict={}  # dictionary with the points in each match
    win_or_lose_binary_dict={} # dict to save if the red boxer wins (1) or loses (0) in each match

    for row_matches in results_matches:
        id_match=row_matches[0]
        id_winner=row_matches[10]
        id_boxer_red=row_matches[2]
        id_boxer_blue=row_matches[3]

        for row_persona in results_persona:
            if row_persona[0]==id_boxer_red:
                gender=row_persona[5]
                if gender=='WOMEN':

                    first_and_second_points=0       # restart for every new match
                    
                    for row_points in results_points:
                        if row_points[2]==id_match and row_points[5]!=None : # condition that the fight had 3 rounds

                            if id_winner==id_boxer_red:
                                win_or_lose_binary_dict[id_match]=1 
                            else:
                                win_or_lose_binary_dict[id_match]=0
                            
                            if row_points[3]==id_boxer_red:  # add points for the red boxer
                                first_and_second_points += row_points[4]
                                first_and_second_points += row_points[5]
                            
                            if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                first_and_second_points -= row_points[4]
                                first_and_second_points -= row_points[5]

                            points_difference_dict[id_match]=first_and_second_points  



    for row_matches in results_matches_panam:
        id_match=row_matches[0]
        id_winner=row_matches[10]
        id_boxer_red=row_matches[2]
        id_boxer_blue=row_matches[3]

        for row_persona in results_persona_panam:
            if row_persona[0]==id_boxer_red:
                gender=row_persona[5]
                if gender=='Women':

                    first_and_second_points=0       # restart for every new match
                    
                    for row_points in results_points_panam:
                        if row_points[2]==id_match and row_points[5]!=0 and row_points[5]!= None: # condition that the fight had 3 rounds

                            if id_winner==id_boxer_red:
                                win_or_lose_binary_dict[id_match]=1 
                            else:
                                win_or_lose_binary_dict[id_match]=0
                            
                            if row_points[3]==id_boxer_red:  # add points for the red boxer
                                first_and_second_points += row_points[4]
                                first_and_second_points += row_points[5]
                            
                            if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                first_and_second_points -= row_points[4]
                                first_and_second_points -= row_points[5]

                            points_difference_dict[id_match]=first_and_second_points  

    
    win_or_lose_list=list(win_or_lose_binary_dict.values())          # list with the result of each of these matches
    points_difference_list=list(points_difference_dict.values())     # list with the difference in point of each of these matches

    element_counts = Counter(points_difference_list)
    different_results_dict = dict(element_counts)  # dictionary with the different in points and the number of times this different happens


    sorted_keys = sorted(different_results_dict.keys())
    rearranged_different_results_dict = {key: different_results_dict[key] for key in sorted_keys}

    different_results_list=list(different_results_dict.keys()) 
    
    rearranged_different_results_list=list(rearranged_different_results_dict.keys()) 
    rearranged_different_results_values_list=list(rearranged_different_results_dict.values())


    positions_dict = {}

    # Loop through the list and populate the dictionary
    for index, value in enumerate(points_difference_list):
        if value not in positions_dict:
            positions_dict[value] = [index]
        else:
            positions_dict[value].append(index)

    mean_dict = {key: np.mean([win_or_lose_list[i] for i in indices]) for key, indices in positions_dict.items()}

    """print('mean_dict')
    print(mean_dict)
    print('win_or_lose_list')
    print(win_or_lose_list)
    print('points_difference_list')
    print(points_difference_list)
    print('positions_dict')
    print(positions_dict)
    print('different_results_list')
    print(different_results_list)"""

    points_difference_mean_list=list(mean_dict.values())   

    popt, pcov = curve_fit(logistic_function, different_results_list, points_difference_mean_list, bounds=([0, 0, 0], [1, 1, 10]))

    x_fit = np.linspace(min(different_results_list), max(different_results_list), 100)
    y_fit = logistic_function(x_fit, *popt)

    print('PARAMETERS:')
    print(popt)
    print('ERRORS WOMEN')
    print(pcov)


    plt.figure()
    plt.scatter(different_results_list, points_difference_mean_list, label='', color='orange')
    plt.plot(x_fit, y_fit, label='Logistic Fit', color='blue')
    plt.xlabel('Points difference in the first two rounds')
    plt.ylabel('Probability of winning')
    plt.legend()
    plt.title('WOMEN SAMPLE')
    plt.grid(False)
    #plt.show()
    plt.savefig('Women sample.png', dpi=300, bbox_inches='tight')
    return(rearranged_different_results_dict)

rearranged_different_results_women_dict=prob_winning_women()

def hypotesis_testing(men_dict, women_dict):

    key_men=list(men_dict.keys()) 
    values_men=list(men_dict.values()) 

    key_women=list(women_dict.keys()) 
    values_women=list(women_dict.values()) 

    men_new_dict={}
    women_new_dict={}

    bin_size= 2
    for i in range(-18,19,bin_size):
        men_new_dict[i]=0
        women_new_dict[i]=0

    for key, value in men_dict.items():
        bin_key = (key // bin_size) * bin_size
        
        if bin_key in men_new_dict:
            men_new_dict[bin_key] += value
        else:
            men_new_dict[bin_key] = value

    for key, value in women_dict.items():
        bin_key = (key // bin_size) * bin_size
        
        if bin_key in women_new_dict:
            women_new_dict[bin_key] += value
        else:
            women_new_dict[bin_key] = value

    key_x=list(men_new_dict.keys()) 

    men=list(men_new_dict.values())
    women=list(women_new_dict.values())

    normalized_men=men/np.sum(men)
    normalized_women=women/np.sum(women)

    print('CHI^2 TEST')
    print(sp.stats.chisquare(normalized_men, f_exp=normalized_women))


    normalized_values_men=values_men/np.sum(values_men)
    normalized_values_women=values_women/np.sum(values_women)
    """print('PERCENTAGE KOLMOGOROV-SMIRNOV')
    print(sp.stats.kstest(normalized_values_men,normalized_values_women))"""

    plt.figure()
    plt.bar(key_men, values_men, color='skyblue')
    plt.xlabel('Points difference in the first two rounds')
    plt.xticks(key_x, rotation=45, fontsize=8)
    plt.legend()
    plt.grid(False)
    plt.title('Difference in points distribution for men')
    plt.savefig('Difference in points distribution for men.png', dpi=300, bbox_inches='tight')

    plt.figure()
    plt.bar(key_women, values_women, color='orange')
    plt.xlabel('Points difference in the first two rounds')
    plt.xticks(key_x, rotation=45, fontsize=8)
    plt.legend()
    plt.grid(False)
    plt.title('Difference in points distribution for women')
    plt.savefig('Difference in points distribution for women.png', dpi=300, bbox_inches='tight')

    plt.figure()
    plt.bar(key_x, men, color='skyblue', label='Men')
    plt.bar(key_x, women, color='orange', label='Women')
    plt.xlabel('Points difference in the first two rounds')
    plt.xticks(key_x, rotation=45, fontsize=8)
    plt.legend()
    plt.grid(False)
    plt.title('Difference in points distribution')
    plt.savefig('Difference in points distribution.png', dpi=300, bbox_inches='tight')

#hypotesis_testing(rearranged_different_results_men_dict, rearranged_different_results_women_dict)

def prob_winning():
    points_difference_dict={}  # dictionary with the points in each match
    win_or_lose_binary_dict={} # dict to save if the red boxer wins (1) or loses (0) in each match

    for row_matches in results_matches:
        id_match=row_matches[0]
        id_winner=row_matches[10]
        id_boxer_red=row_matches[2]
        id_boxer_blue=row_matches[3]

        for row_persona in results_persona:
            if row_persona[0]==id_boxer_red:

                first_and_second_points=0       # restart for every new match
                
                for row_points in results_points:
                    if row_points[2]==id_match and row_points[5]!=0 and row_points[5]!= None: # condition that the fight had 3 rounds

                        if id_winner==id_boxer_red:
                            win_or_lose_binary_dict[id_match]=1 
                        else:
                            win_or_lose_binary_dict[id_match]=0
                        
                        if row_points[3]==id_boxer_red:  # add points for the red boxer
                            first_and_second_points += row_points[4]
                            first_and_second_points += row_points[5]
                        
                        if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                            first_and_second_points -= row_points[4]
                            first_and_second_points -= row_points[5]

                        points_difference_dict[id_match]=first_and_second_points  



    for row_matches in results_matches_panam:
        id_match=row_matches[0]
        id_winner=row_matches[10]
        id_boxer_red=row_matches[2]
        id_boxer_blue=row_matches[3]

        for row_persona in results_persona_panam:
            if row_persona[0]==id_boxer_red:

                first_and_second_points=0       # restart for every new match
                
                for row_points in results_points_panam:
                    if row_points[2]==id_match and row_points[5]!=None: # condition that the fight had 3 rounds

                        if id_winner==id_boxer_red:
                            win_or_lose_binary_dict[id_match]=1 
                        else:
                            win_or_lose_binary_dict[id_match]=0
                        
                        if row_points[3]==id_boxer_red:  # add points for the red boxer
                            first_and_second_points += row_points[4]
                            first_and_second_points += row_points[5]
                        
                        if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                            first_and_second_points -= row_points[4]
                            first_and_second_points -= row_points[5]

                        points_difference_dict[id_match]=first_and_second_points 

    
    win_or_lose_list=list(win_or_lose_binary_dict.values())          # list with the result of each of these matches
    points_difference_list=list(points_difference_dict.values())     # list with the difference in point of each of these matches

    element_counts = Counter(points_difference_list)
    different_results_dict = dict(element_counts)  # dictionary with the different in points and the number of times this different happens

    sorted_keys = sorted(different_results_dict.keys())
    rearranged_different_results_dict = {key: different_results_dict[key] for key in sorted_keys}

    different_results_list=list(different_results_dict.keys()) 

    rearranged_different_results_list=list(rearranged_different_results_dict.keys()) 
    rearranged_different_results_values_list=list(rearranged_different_results_dict.values()) 


    positions_dict = {}

    # Loop through the list and populate the dictionary
    for index, value in enumerate(points_difference_list):
        if value not in positions_dict:
            positions_dict[value] = [index]
        else:
            positions_dict[value].append(index)

    mean_dict = {key: np.mean([win_or_lose_list[i] for i in indices]) for key, indices in positions_dict.items()}

    """print('mean_dict')
    print(mean_dict)
    print('win_or_lose_list')
    print(win_or_lose_list)
    print('points_difference_list')
    print(points_difference_list)
    print('positions_dict')
    print(positions_dict)
    print('different_results_list')
    print(different_results_list)"""

    points_difference_mean_list=list(mean_dict.values())   

    popt, pcov = curve_fit(logistic_function, different_results_list, points_difference_mean_list, bounds=([0, 0, 0], [1, 1, 10]))

    x_fit = np.linspace(min(different_results_list), max(different_results_list), 100)
    y_fit = logistic_function(x_fit, *popt)

    print('PARAMETERS TOTAL:')
    print(popt)
    print('ERRORS TOTAL')
    print(pcov)

    plt.figure()
    plt.scatter(different_results_list, points_difference_mean_list, label='', color='black')
    plt.plot(x_fit, y_fit, label='Logistic Fit', color='red')
    plt.xlabel('Points difference in the first two rounds')
    plt.ylabel('Probability of winning')
    plt.title('')
    plt.legend()
    plt.grid(False)
    #plt.show()
    plt.savefig('All sample.png', dpi=300, bbox_inches='tight')

    return(rearranged_different_results_list, rearranged_different_results_values_list)

#prob_winning()

def prob_weight():

    weight_difference_dict={}  # dictionary with the points in each match
    win_or_lose_binary_dict={} # dict to save if the red boxer wins (1) or loses (0) in each match
    weight_list=[51.0, 57.0, 63.5, 71.0, 80.0, 92.0, 50.0, 54.0, 57.0, 60.0, 66.0, 75.0] # list of not interesting weights

    for row_matches in results_matches:
        id_match=row_matches[0]
        id_winner=row_matches[10]
        id_boxer_red=row_matches[2]
        id_boxer_blue=row_matches[3]

        difference=False

        for row_persona in results_persona:
            
            if row_persona[0]==id_boxer_red:
                weight=row_persona[4]
            
                if weight not in weight_list:
                    weight_red=row_persona[4]

            elif id_boxer_blue==row_persona[0]:
                weight=row_persona[4]

                if weight not in weight_list:
                    weight_blue=row_persona[4]
                    difference=True
        
        if difference==True:
            weight_difference_dict[id_match]=weight_red-weight_blue

            if id_winner==id_boxer_red:
                win_or_lose_binary_dict[id_match]=1 
            else:
                win_or_lose_binary_dict[id_match]=0
                                        
    
    win_or_lose_list=list(win_or_lose_binary_dict.values())          # list with the result of each of these matches
    weight_difference_list=list(weight_difference_dict.values())     # list with the difference in point of each of these matches

    print(len(win_or_lose_binary_dict))
    print(weight_difference_list)

    element_counts = Counter(weight_difference_list)
    different_results_dict = dict(element_counts)  # dictionary with the different in weight and the number of times this different happens

    sorted_keys = sorted(different_results_dict.keys())
    rearranged_different_results_dict = {key: different_results_dict[key] for key in sorted_keys}

    different_results_list=list(different_results_dict.keys()) 

    rearranged_different_results_list=list(rearranged_different_results_dict.keys()) 
    rearranged_different_results_values_list=list(rearranged_different_results_dict.values()) 


    positions_dict = {}

    # Loop through the list and populate the dictionary
    for index, value in enumerate(weight_difference_list):
        if value not in positions_dict:
            positions_dict[value] = [index]
        else:
            positions_dict[value].append(index)

    mean_dict = {key: np.mean([win_or_lose_list[i] for i in indices]) for key, indices in positions_dict.items()}

    """print('mean_dict')
    print(mean_dict)
    print('win_or_lose_list')
    print(win_or_lose_list)
    print('weight_difference_list')
    print(weight_difference_list)
    print('positions_dict')
    print(positions_dict)
    print('different_results_list')
    print(different_results_list)"""

    weight_difference_mean_list=list(mean_dict.values())   

    popt, pcov = curve_fit(logistic_function, different_results_list, weight_difference_mean_list, bounds=([0, 0, 0], [1, 1, 10]))

    x_fit = np.linspace(min(different_results_list), max(different_results_list), 100)
    y_fit = logistic_function(x_fit, *popt)

    print('PARAMETERS WEIGHT:')
    print(popt)
    print('ERRORS WEIGHT')
    print(pcov)

    plt.figure()
    plt.scatter(different_results_list, weight_difference_mean_list, label='', color='green')
    plt.plot(x_fit, y_fit, label='Logistic Fit', color='black')
    plt.xlabel('Weight difference')
    plt.ylabel('Probability of winning')
    plt.title('+92kg SAMPLE')
    plt.legend()
    plt.grid(False)
    #plt.show()
    plt.savefig('Over 92 kg sample.png', dpi=300, bbox_inches='tight')

    return(rearranged_different_results_list, rearranged_different_results_values_list)

#prob_weight()

def prob_year():
    year_difference_dict={}  # dictionary with the points in each match
    win_or_lose_binary_dict={} # dict to save if the red boxer wins (1) or loses (0) in each match

    for row_matches in results_matches:
        id_match=row_matches[0]
        id_winner=row_matches[10]
        id_boxer_red=row_matches[2]
        id_boxer_blue=row_matches[3]

        if id_winner==id_boxer_red:
            win_or_lose_binary_dict[id_match]=1 
        else:
            win_or_lose_binary_dict[id_match]=0

        difference=False

        for row_persona in results_persona:
            
            if row_persona[0]==id_boxer_red:
                
                year_red=row_persona[3]

            elif id_boxer_blue==row_persona[0]:
                
                year_blue=row_persona[3]
                difference=True
        
        if difference==True:
            year_difference_dict[id_match]=year_red-year_blue



    for row_matches in results_matches_panam:
        id_match=row_matches[0]
        id_winner=row_matches[10]
        id_boxer_red=row_matches[2]
        id_boxer_blue=row_matches[3]

        if id_winner==id_boxer_red:
            win_or_lose_binary_dict[id_match]=1 
        else:
            win_or_lose_binary_dict[id_match]=0

        difference=False

        for row_persona in results_persona_panam:
            
            if row_persona[0]==id_boxer_red:
                
                year_red=row_persona[3]

            elif id_boxer_blue==row_persona[0]:
                
                year_blue=row_persona[3]
                difference=True
        
        if difference==True:
            year_difference_dict[id_match]=year_red-year_blue

            
                                        
    
    win_or_lose_list=list(win_or_lose_binary_dict.values())          # list with the result of each of these matches
    year_difference_list=list(year_difference_dict.values())     # list with the difference in point of each of these matches

    element_counts = Counter(year_difference_list)
    different_results_dict = dict(element_counts)  # dictionary with the different in year and the number of times this different happens

    sorted_keys = sorted(different_results_dict.keys())
    rearranged_different_results_dict = {key: different_results_dict[key] for key in sorted_keys}

    different_results_list=list(different_results_dict.keys()) 

    rearranged_different_results_list=list(rearranged_different_results_dict.keys()) 
    rearranged_different_results_values_list=list(rearranged_different_results_dict.values()) 


    positions_dict = {}

    # Loop through the list and populate the dictionary
    for index, value in enumerate(year_difference_list):
        if value not in positions_dict:
            positions_dict[value] = [index]
        else:
            positions_dict[value].append(index)

    mean_dict = {key: np.mean([win_or_lose_list[i] for i in indices]) for key, indices in positions_dict.items()}

    """print('mean_dict')
    print(mean_dict)
    print('win_or_lose_list')
    print(win_or_lose_list)
    print('year_difference_list')
    print(year_difference_list)
    print('positions_dict')
    print(positions_dict)
    print('different_results_list')
    print(different_results_list)"""

    year_difference_mean_list=list(mean_dict.values())   

    popt, pcov = curve_fit(logistic_function, different_results_list, year_difference_mean_list, bounds=([0, 0, 0], [1, 1, 10]))

    x_fit = np.linspace(min(different_results_list), max(different_results_list), 100)
    y_fit = logistic_function(x_fit, *popt)

    print('PARAMETERS YEAR:')
    print(popt)
    print('ERRORS YEAR')
    print(pcov)

    plt.figure()
    plt.scatter(different_results_list, year_difference_mean_list, label='', color='red')
    #plt.plot(x_fit, y_fit, label='Logistic Fit', color='green')
    plt.xlabel('Year difference')
    plt.ylabel('Probability of winning')
    plt.title('YEAR SAMPLE')
    plt.legend()
    plt.grid(False)
    #plt.show()
    plt.savefig('Year sample.png', dpi=300, bbox_inches='tight')

    return(rearranged_different_results_list, rearranged_different_results_values_list)

#prob_year()

def prob_winning_ko_men():


    points_difference_dict={}  # dictionary with the points in each match
    win_or_lose_binary_dict={} # dict to save if the red boxer wins (1) or loses (0) in each match

    for row_matches in results_matches:
        if row_matches[-2]=='RSC' or row_matches[-2]=='KO':
            result= re.search(r'^[^\d]+[\d.]*', row_matches[-1])
            result_string=result.group()
            if result_string=='R3':
                id_match=row_matches[0]
                id_winner=row_matches[10]
                id_boxer_red=row_matches[2]
                id_boxer_blue=row_matches[3]

                for row_persona in results_persona:
                    if row_persona[0]==id_boxer_red:
                        gender=row_persona[5]
                        if gender=='MEN':

                            first_and_second_points=0       # restart for every new match
                            
                            for row_points in results_points:
                                if row_points[2]==id_match and row_points[5]!=None: # condition that the fight had 2 completed rounds

                                    if id_winner==id_boxer_red:
                                        win_or_lose_binary_dict[id_match]=1 
                                    else:
                                        win_or_lose_binary_dict[id_match]=0
                                    
                                    if row_points[3]==id_boxer_red:  # add points for the red boxer
                                        first_and_second_points += row_points[4]
                                        first_and_second_points += row_points[5]
                                    
                                    if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                        first_and_second_points -= row_points[4]
                                        first_and_second_points -= row_points[5]

                                    points_difference_dict[id_match]=first_and_second_points  

    for row_matches in results_matches_panam:
        if row_matches[-2]=='RSC' or row_matches[-2]=='KO':
            result= re.search(r'^[^\d]+[\d.]*', row_matches[-1])
            result_string=result.group()
            if result_string=='R3':
                id_match=row_matches[0]
                id_winner=row_matches[10]
                id_boxer_red=row_matches[2]
                id_boxer_blue=row_matches[3]

                for row_persona in results_persona_panam:
                    if row_persona[0]==id_boxer_red:
                        gender=row_persona[5]
                        if gender=='Men':

                            first_and_second_points=0       # restart for every new match
                            
                            for row_points in results_points_panam:
                                if row_points[2]==id_match and row_points[5]!=None: # condition that the fight had 2 completed rounds

                                    if id_winner==id_boxer_red:
                                        win_or_lose_binary_dict[id_match]=1 
                                    else:
                                        win_or_lose_binary_dict[id_match]=0
                                    
                                    if row_points[3]==id_boxer_red:  # add points for the red boxer
                                        first_and_second_points += row_points[4]
                                        first_and_second_points += row_points[5]
                                    
                                    if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                        first_and_second_points -= row_points[4]
                                        first_and_second_points -= row_points[5]

                                    points_difference_dict[id_match]=first_and_second_points  

    
    win_or_lose_list=list(win_or_lose_binary_dict.values())          # list with the result of each of these matches
    points_difference_list=list(points_difference_dict.values())     # list with the difference in point of each of these matches

    element_counts = Counter(points_difference_list)
    different_results_dict = dict(element_counts)  # dictionary with the different in points and the number of times this different happens

    sorted_keys = sorted(different_results_dict.keys())
    rearranged_different_results_dict = {key: different_results_dict[key] for key in sorted_keys}

    different_results_list=list(different_results_dict.keys()) 

    rearranged_different_results_list=list(rearranged_different_results_dict.keys()) 
    rearranged_different_results_values_list=list(rearranged_different_results_dict.values()) 


    positions_dict = {}

    # Loop through the list and populate the dictionary
    for index, value in enumerate(points_difference_list):
        if value not in positions_dict:
            positions_dict[value] = [index]
        else:
            positions_dict[value].append(index)

    

    mean_dict = {key: np.mean([win_or_lose_list[i] for i in indices]) for key, indices in positions_dict.items()}

    """print('mean_dict')
    print(mean_dict)
    print('win_or_lose_list')
    print(win_or_lose_list)
    print('points_difference_list')
    print(points_difference_list)
    print('positions_dict')
    print(positions_dict)
    print('different_results_list')
    print(different_results_list)"""

    points_difference_mean_list=list(mean_dict.values())   

    print('First check')
    print(len(points_difference_mean_list))


    popt, pcov = curve_fit(logistic_function, different_results_list, points_difference_mean_list, bounds=([0, 0, 0], [1, 1, 10]))

    x_fit = np.linspace(min(different_results_list), max(different_results_list), 100)
    y_fit = logistic_function(x_fit, *popt)

    print('PARAMETERS TECHNICAL KO MEN:')
    print(popt)
    print('ERRORS THECNICAL KO MEN')
    print(pcov)

    plt.figure()
    plt.scatter(different_results_list, points_difference_mean_list, label='')
    plt.plot(x_fit, y_fit, label='Logistic Fit', color='orange')
    plt.xlabel('Points difference in the first two rounds')
    plt.ylabel('Probability of winning by KO')
    plt.title('MEN TECHNICAL KO SAMPLE')
    plt.legend()
    plt.grid(False)
    #plt.show()
    plt.savefig('Men sample ko.png', dpi=300, bbox_inches='tight')

    return(rearranged_different_results_dict)

prob_winning_ko_men()

def prob_winning_ko_women():


    points_difference_dict={}  # dictionary with the points in each match
    win_or_lose_binary_dict={} # dict to save if the red boxer wins (1) or loses (0) in each match
    counter=0
    for row_matches in results_matches:
        if row_matches[-2]=='RSC' or row_matches[-2]=='KO':
            result= re.search(r'^[^\d]+[\d.]*', row_matches[-1])
            result_string=result.group()
            if result_string=='R3':
                id_match=row_matches[0]
                id_winner=row_matches[10]
                id_boxer_red=row_matches[2]
                id_boxer_blue=row_matches[3]

                for row_persona in results_persona:
                    if row_persona[0]==id_boxer_red:
                        gender=row_persona[5]
                        if gender=='WOMEN':
                            
                            first_and_second_points=0       # restart for every new match
                            
                            for row_points in results_points:
                                if row_points[2]==id_match and row_points[5]!=None: # condition that the fight had 2 completed rounds
                                    counter+=1
                                    if id_winner==id_boxer_red:
                                        win_or_lose_binary_dict[id_match]=1 
                                    else:
                                        win_or_lose_binary_dict[id_match]=0
                                    
                                    if row_points[3]==id_boxer_red:  # add points for the red boxer
                                        first_and_second_points += row_points[4]
                                        first_and_second_points += row_points[5]
                                    
                                    if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                        first_and_second_points -= row_points[4]
                                        first_and_second_points -= row_points[5]

                                    points_difference_dict[id_match]=first_and_second_points 

    for row_matches in results_matches_panam:
        if row_matches[-2]=='RSC' or row_matches[-2]=='KO':
            result= re.search(r'^[^\d]+[\d.]*', row_matches[-1])
            result_string=result.group()
            if result_string=='R3':
                id_match=row_matches[0]
                id_winner=row_matches[10]
                id_boxer_red=row_matches[2]
                id_boxer_blue=row_matches[3]

                for row_persona in results_persona_panam:
                    if row_persona[0]==id_boxer_red:
                        gender=row_persona[5]
                        if gender=='Women':

                            first_and_second_points=0       # restart for every new match
                            
                            for row_points in results_points_panam:
                                if row_points[2]==id_match and row_points[5]!=None: # condition that the fight had 2 completed rounds
                                    counter+=1
                                    if id_winner==id_boxer_red:
                                        win_or_lose_binary_dict[id_match]=1 
                                    else:
                                        win_or_lose_binary_dict[id_match]=0
                                    
                                    if row_points[3]==id_boxer_red:  # add points for the red boxer
                                        first_and_second_points += row_points[4]
                                        first_and_second_points += row_points[5]
                                    
                                    if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                        first_and_second_points -= row_points[4]
                                        first_and_second_points -= row_points[5]

                                    points_difference_dict[id_match]=first_and_second_points   

    
    win_or_lose_list=list(win_or_lose_binary_dict.values())          # list with the result of each of these matches
    points_difference_list=list(points_difference_dict.values())     # list with the difference in point of each of these matches

    element_counts = Counter(points_difference_list)
    different_results_dict = dict(element_counts)  # dictionary with the different in points and the number of times this different happens

    sorted_keys = sorted(different_results_dict.keys())
    rearranged_different_results_dict = {key: different_results_dict[key] for key in sorted_keys}

    different_results_list=list(different_results_dict.keys()) 

    rearranged_different_results_list=list(rearranged_different_results_dict.keys()) 
    rearranged_different_results_values_list=list(rearranged_different_results_dict.values()) 


    positions_dict = {}

    # Loop through the list and populate the dictionary
    for index, value in enumerate(points_difference_list):
        if value not in positions_dict:
            positions_dict[value] = [index]
        else:
            positions_dict[value].append(index)

    

    mean_dict = {key: np.mean([win_or_lose_list[i] for i in indices]) for key, indices in positions_dict.items()}

    """print('mean_dict')
    print(mean_dict)
    print('win_or_lose_list')
    print(win_or_lose_list)
    print('points_difference_list')
    print(points_difference_list)
    print('positions_dict')
    print(positions_dict)
    print('different_results_list')
    print(different_results_list)"""

    points_difference_mean_list=list(mean_dict.values())   

    popt, pcov = curve_fit(logistic_function, different_results_list, points_difference_mean_list, bounds=([0, 0, 0], [1, 1, 10]))

    x_fit = np.linspace(min(different_results_list), max(different_results_list), 100)
    y_fit = logistic_function(x_fit, *popt)

    print('NUMBER OF FIGHTS IN KO WOMEN:')
    print(counter)
    print('#########################################')
    print('PARAMETERS TECHNICAL KO WOMEN:')
    print(popt)
    print('ERRORS TECHNICAL KO WOMEN')
    print(pcov)

    plt.figure()
    plt.scatter(different_results_list, points_difference_mean_list, label='')
    plt.plot(x_fit, y_fit, label='Logistic Fit', color='orange')
    plt.xlabel('Points difference in the first two rounds')
    plt.ylabel('Probability of winning by KO')
    plt.title('WOMEN TECHNICAL KO SAMPLE')
    plt.legend()
    plt.grid(False)
    #plt.show()
    plt.savefig('Women_sample_ko.png', dpi=300, bbox_inches='tight')

    return(rearranged_different_results_dict)

prob_winning_ko_women()

def prob_winning_ko_men_round_1():


    points_difference_dict={}  # dictionary with the points in each match
    win_or_lose_binary_dict={} # dict to save if the red boxer wins (1) or loses (0) in each match

    for row_matches in results_matches:
        if row_matches[-2]=='RSC' or row_matches[-2]=='KO':
            result= re.search(r'^[^\d]+[\d.]*', row_matches[-1])
            result_string=result.group()
            if result_string=='R3' or result_string=='R2':
                id_match=row_matches[0]
                id_winner=row_matches[10]
                id_boxer_red=row_matches[2]
                id_boxer_blue=row_matches[3]

                for row_persona in results_persona:
                    if row_persona[0]==id_boxer_red:
                        gender=row_persona[5]
                        if gender=='MEN':

                            first_and_second_points=0       # restart for every new match
                            
                            for row_points in results_points:
                                if row_points[2]==id_match and row_points[4]!=None: # condition that the fight had 1 completed round

                                    if id_winner==id_boxer_red:
                                        win_or_lose_binary_dict[id_match]=1 
                                    else:
                                        win_or_lose_binary_dict[id_match]=0
                                    
                                    if row_points[3]==id_boxer_red:  # add points for the red boxer
                                        first_and_second_points += row_points[4]
                                    
                                    if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                        first_and_second_points -= row_points[4]

                                    points_difference_dict[id_match]=first_and_second_points  

    for row_matches in results_matches_panam:
        if row_matches[-2]=='RSC' or row_matches[-2]=='KO':
            result= re.search(r'^[^\d]+[\d.]*', row_matches[-1])
            result_string=result.group()
            if result_string=='R3' or result_string=='"R2':
                id_match=row_matches[0]
                id_winner=row_matches[10]
                id_boxer_red=row_matches[2]
                id_boxer_blue=row_matches[3]

                for row_persona in results_persona_panam:
                    if row_persona[0]==id_boxer_red:
                        gender=row_persona[5]
                        if gender=='Men':

                            first_and_second_points=0       # restart for every new match
                            
                            for row_points in results_points_panam:
                                if row_points[2]==id_match and row_points[4]!=None: # condition that the fight had 1 completed round

                                    if id_winner==id_boxer_red:
                                        win_or_lose_binary_dict[id_match]=1 
                                    else:
                                        win_or_lose_binary_dict[id_match]=0
                                    
                                    if row_points[3]==id_boxer_red:  # add points for the red boxer
                                        first_and_second_points += row_points[4]
                                    
                                    if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                        first_and_second_points -= row_points[4]

                                    points_difference_dict[id_match]=first_and_second_points  

    
    win_or_lose_list=list(win_or_lose_binary_dict.values())          # list with the result of each of these matches
    points_difference_list=list(points_difference_dict.values())     # list with the difference in point of each of these matches

    element_counts = Counter(points_difference_list)
    different_results_dict = dict(element_counts)  # dictionary with the different in points and the number of times this different happens

    sorted_keys = sorted(different_results_dict.keys())
    rearranged_different_results_dict = {key: different_results_dict[key] for key in sorted_keys}

    different_results_list=list(different_results_dict.keys()) 

    rearranged_different_results_list=list(rearranged_different_results_dict.keys()) 
    rearranged_different_results_values_list=list(rearranged_different_results_dict.values()) 


    positions_dict = {}

    # Loop through the list and populate the dictionary
    for index, value in enumerate(points_difference_list):
        if value not in positions_dict:
            positions_dict[value] = [index]
        else:
            positions_dict[value].append(index)

    

    mean_dict = {key: np.mean([win_or_lose_list[i] for i in indices]) for key, indices in positions_dict.items()}

    """print('mean_dict')
    print(mean_dict)
    print('win_or_lose_list')
    print(win_or_lose_list)
    print('points_difference_list')
    print(points_difference_list)
    print('positions_dict')
    print(positions_dict)
    print('different_results_list')
    print(different_results_list)"""

    points_difference_mean_list=list(mean_dict.values())   

    print('First check')
    print(len(points_difference_mean_list))


    popt, pcov = curve_fit(logistic_function, different_results_list, points_difference_mean_list, bounds=([0, 0, 0], [1, 1, 10]))

    x_fit = np.linspace(min(different_results_list), max(different_results_list), 100)
    y_fit = logistic_function(x_fit, *popt)

    print('PARAMETERS R1 TECHNICAL KO MEN:')
    print(popt)
    print('ERRORS R1 THECNICAL KO MEN')
    print(pcov)

    plt.figure()
    plt.scatter(different_results_list, points_difference_mean_list, label='')
    plt.plot(x_fit, y_fit, label='Logistic Fit', color='orange')
    plt.xlabel('Points difference in the first round')
    plt.ylabel('Probability of winning by KO')
    plt.title('MEN TECHNICAL KO SAMPLE')
    plt.legend()
    plt.grid(False)
    #plt.show()
    plt.savefig('Men sample ko R1.png', dpi=300, bbox_inches='tight')

    return(rearranged_different_results_dict)

prob_winning_ko_men_round_1()


def prob_winning_ko_women_round_1():


    points_difference_dict={}  # dictionary with the points in each match
    win_or_lose_binary_dict={} # dict to save if the red boxer wins (1) or loses (0) in each match

    for row_matches in results_matches:
        if row_matches[-2]=='RSC' or row_matches[-2]=='KO':
            result= re.search(r'^[^\d]+[\d.]*', row_matches[-1])
            result_string=result.group()
            if result_string=='R3' or result_string=='R2':
                id_match=row_matches[0]
                id_winner=row_matches[10]
                id_boxer_red=row_matches[2]
                id_boxer_blue=row_matches[3]

                for row_persona in results_persona:
                    if row_persona[0]==id_boxer_red:
                        gender=row_persona[5]
                        if gender=='WOMEN':

                            first_and_second_points=0       # restart for every new match
                            
                            for row_points in results_points:
                                if row_points[2]==id_match and row_points[4]!=None: # condition that the fight had 1 completed round

                                    if id_winner==id_boxer_red:
                                        win_or_lose_binary_dict[id_match]=1 
                                    else:
                                        win_or_lose_binary_dict[id_match]=0
                                    
                                    if row_points[3]==id_boxer_red:  # add points for the red boxer
                                        first_and_second_points += row_points[4]
                                    
                                    if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                        first_and_second_points -= row_points[4]

                                    points_difference_dict[id_match]=first_and_second_points 

    for row_matches in results_matches_panam:
        if row_matches[-2]=='RSC' or row_matches[-2]=='KO':
            result= re.search(r'^[^\d]+[\d.]*', row_matches[-1])
            result_string=result.group()
            if result_string=='R3' or result_string=='R2':
                id_match=row_matches[0]
                id_winner=row_matches[10]
                id_boxer_red=row_matches[2]
                id_boxer_blue=row_matches[3]

                for row_persona in results_persona_panam:
                    if row_persona[0]==id_boxer_red:
                        gender=row_persona[5]
                        if gender=='Women':

                            first_and_second_points=0       # restart for every new match
                            
                            for row_points in results_points_panam:
                                if row_points[2]==id_match and row_points[5]!=None: # condition that the fight had 1 completed round

                                    if id_winner==id_boxer_red:
                                        win_or_lose_binary_dict[id_match]=1 
                                    else:
                                        win_or_lose_binary_dict[id_match]=0
                                    
                                    if row_points[3]==id_boxer_red:  # add points for the red boxer
                                        first_and_second_points += row_points[4]
                                    
                                    if row_points[3]==id_boxer_blue: # substract points for the blue boxer
                                        first_and_second_points -= row_points[4]

                                    points_difference_dict[id_match]=first_and_second_points   

    
    win_or_lose_list=list(win_or_lose_binary_dict.values())          # list with the result of each of these matches
    points_difference_list=list(points_difference_dict.values())     # list with the difference in point of each of these matches

    element_counts = Counter(points_difference_list)
    different_results_dict = dict(element_counts)  # dictionary with the different in points and the number of times this different happens

    sorted_keys = sorted(different_results_dict.keys())
    rearranged_different_results_dict = {key: different_results_dict[key] for key in sorted_keys}

    different_results_list=list(different_results_dict.keys()) 

    rearranged_different_results_list=list(rearranged_different_results_dict.keys()) 
    rearranged_different_results_values_list=list(rearranged_different_results_dict.values()) 


    positions_dict = {}

    # Loop through the list and populate the dictionary
    for index, value in enumerate(points_difference_list):
        if value not in positions_dict:
            positions_dict[value] = [index]
        else:
            positions_dict[value].append(index)

    

    mean_dict = {key: np.mean([win_or_lose_list[i] for i in indices]) for key, indices in positions_dict.items()}

    """print('mean_dict')
    print(mean_dict)
    print('win_or_lose_list')
    print(win_or_lose_list)
    print('points_difference_list')
    print(points_difference_list)
    print('positions_dict')
    print(positions_dict)
    print('different_results_list')
    print(different_results_list)"""

    points_difference_mean_list=list(mean_dict.values())   

    popt, pcov = curve_fit(logistic_function, different_results_list, points_difference_mean_list, bounds=([0, 0, 0], [1, 1, 10]))

    x_fit = np.linspace(min(different_results_list), max(different_results_list), 100)
    y_fit = logistic_function(x_fit, *popt)

    print('PARAMETERS R1 TECHNICAL KO WOMEN:')
    print(popt)
    print('ERRORS R1 TECHNICAL KO WOMEN')
    print(pcov)

    plt.figure()
    plt.scatter(different_results_list, points_difference_mean_list, label='')
    plt.plot(x_fit, y_fit, label='Logistic Fit', color='orange')
    plt.xlabel('Points difference in the first round')
    plt.ylabel('Probability of winning by KO')
    plt.title('WOMEN TECHNICAL KO SAMPLE')
    plt.legend()
    plt.grid(False)
    #plt.show()
    plt.savefig('Women_sample_ko_R1.png', dpi=300, bbox_inches='tight')

    return(rearranged_different_results_dict)

prob_winning_ko_women_round_1()
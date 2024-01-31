import mysql.connector
from collections import Counter
import numpy as np
from scipy.stats import chisquare
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import levene
from scipy import stats

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

def id_matches(row):
    id_match=[]

    for i in range(len(row)-4):
        id_match.append(row[i])
    
    return id_match

    
def round_points(row):
    round_list=[]

    for i in range(4,7):
        round_list.append(row[i])
    return round_list

        

def nationalities_matrix():

    judge_nationality_dict={}
    boxer_nationality_dict={}

    # loop to create all the keys for boxer's nationality and judge's nationality
    for row_persona in results_persona:
        if row_persona[-1]=='boxer':
            if row_persona[2] not in boxer_nationality_dict:
                boxer_nationality_dict[row_persona[2]]=0
        
        if row_persona[-1]=='judge':
            if row_persona[2] not in judge_nationality_dict:
                judge_nationality_dict[row_persona[2]]=0

    judge_nationality_list=list(judge_nationality_dict.keys())  
    boxer_nationality_list=list(boxer_nationality_dict.keys()) 

    # matrixes with the same number of rows as judge_nationality_list and same number of columns as boxer_nationality_list
    matrix_count_nationalities=[[0 for _ in range(len(boxer_nationality_list))] for _ in range(len(judge_nationality_list))]
    matrix_normalized_nationalities=[[0 for _ in range(len(boxer_nationality_list))] for _ in range(len(judge_nationality_list))]

    
    for row_matches in results_matches:
        match_list=id_matches(row_matches) # [id, phase, id_boxer_red, id_boxer_blue, id_judge_1, id_judge_2, id_judge_3, id_judge_4, id_judge_5]
        nationality_judge=[]

        for row_persona in results_persona: # obtain the nationality of the boxers and judges
                            
            if match_list[2]==row_persona[0]:
                nationality_red_boxer=row_persona[2] # red boxer
            elif match_list[3]==row_persona[0]:
                nationality_blue_boxer=row_persona[2] # blue boxer

            for i in range(4,9): # [id_judge_1, id_judge_2, id_judge_3, id_judge_4, id_judge_5]
                if match_list[i]==row_persona[0]:
                    nationality_judge.append(row_persona[2]) #list with the judges
            counter=0

        for row_points in results_points: # look in the points table
            
            if row_points[2]==match_list[0]: # look for the fight
                if counter==0:
                    round_red=round_points(row_points)  # ['points_1', 'points_2', 'points_3'] red points list
                    counter=1
                    

                elif counter==1:
                    round_blue=round_points(row_points) # ['points_1', 'points_2', 'points_3'] blue points list

                    counter=0
                    difference_in_each_round = [x - y for x, y in zip(round_red, round_blue) if x is not None and y is not None]
                    

                    position_id = match_list.index(row_points[1])   # look for the judge in the match_list

                    nationality =nationality_judge[position_id-4]     # look for the nationality

                    i=judge_nationality_list.index(nationality)                 # index of the judge nationality in the whole list of judge nationalities
                    j_red=boxer_nationality_list.index(nationality_red_boxer)   # index of the red nationality in the whole list of judge nationalitie
                    j_blue=boxer_nationality_list.index(nationality_blue_boxer) # index of the blue nationality in the whole list of judge nationalitie

                    matrix_count_nationalities[i][j_red] +=3 # count of the rounds
                    matrix_count_nationalities[i][j_blue] +=3

                    matrix_normalized_nationalities[i][j_red] += np.sum(difference_in_each_round)
                    matrix_normalized_nationalities[i][j_blue] += -np.sum(difference_in_each_round)

    result_matrix = []

    # Normalization of the matrix
    for row1, row2 in zip(matrix_normalized_nationalities, matrix_count_nationalities):
        row_result = []
        for elem1, elem2 in zip(row1, row2):
            if elem2!=0:
                row_result.append(elem1 / elem2)
            else:
                row_result.append(0)
        result_matrix.append(row_result)

    """for row in result_matrix:
        print(row)"""

    result_matrix=np.array(result_matrix)

    num_permutations = 10000

    # Matrix of p-values
    
    dimensions = np.shape(result_matrix)
    rows_result_matrix, columns_result_matrix = dimensions
    
    p_value_matrix=np.empty((rows_result_matrix, columns_result_matrix))
    
    for j in range(rows_result_matrix): 
        # array with the same length as the rows to save the number of times the shuffled values are larger than the real one
        save_array=np.zeros(columns_result_matrix)     
                                            
        for i in range(num_permutations):
            row_shuffled=result_matrix[j,:]
            shuffle_completed=np.random.permutation(row_shuffled)
            for k in range(len(save_array)):
                if shuffle_completed[k]>=result_matrix[j,k]:
                    save_array[k]+=1
        p_value_array=[x/num_permutations for x in save_array]
        p_value_matrix[j, :] = p_value_array
    
    p_value_matrix_low=np.empty((rows_result_matrix, columns_result_matrix))

    result_matrix_low=-1*result_matrix
    
    for j in range(rows_result_matrix): 
        # array with the same length as the rows to save the number of times the shuffled values are larger than the real one
        save_array_low=np.zeros(columns_result_matrix)     
                                            
        for i in range(num_permutations):
            row_shuffled_low=result_matrix_low[j,:]
            shuffle_completed_low=np.random.permutation(row_shuffled_low)
            for k in range(len(save_array_low)):
                if shuffle_completed_low[k]>=result_matrix_low[j,k]:
                    save_array_low[k]+=1
        p_value_array_low=[x/num_permutations for x in save_array_low]
        p_value_matrix_low[j, :] = p_value_array_low
    
    p_value_matrix_low=-p_value_matrix_low 
        
    ###########################     OPTION 1    #################################################################
        
    num_columns = len(p_value_matrix[0])

    number_of_p=[]

    for j in range(num_columns):
        extreme_cases = np.array(p_value_matrix)[:, j]
        number_of_p.append(np.sum(extreme_cases <= 0.05)) # number of significant p-values in each column
    

    greater_p=max(number_of_p)
    extreme_technique_array=[i for i, n in enumerate(number_of_p) if n == greater_p]  # position of the columns with greater number of sig. p-values

    print('Most probable skilled countries:')
    print(len(extreme_technique_array))

    extreme_imparciality_array=[i for i, n in enumerate(number_of_p) if n == 1]   # position of the columns with just one sig. p-value
    print('Most probable unfair benefitiated countries:')
    print(len(extreme_imparciality_array))

    difference_array=[]

    for values in extreme_imparciality_array:     # loop to obtain the distribution with more diference between the significant p-value and the rest
        comparation_array=np.array(p_value_matrix)[:,values]
        low_value=min(comparation_array)
        comparation_array=comparation_array[comparation_array!=low_value]
        difference_array.append(np.mean(comparation_array)-low_value)

    worst_case=np.argmax(np.array(difference_array)) # position of the element with maximum difference in the extreme_imp. array
    removed_elem=extreme_imparciality_array[worst_case] # position of the element with maximum difference in number_of_p

    print('The final most unjust case:')
    print(boxer_nationality_list[removed_elem])

    difference_high_array=[]
    for values in extreme_technique_array:     # loop to obtain the distribution with more diference between the significant p-value and the rest
        comparation_high_array=np.array(p_value_matrix)[:,values]
        low_values_array=comparation_high_array[comparation_high_array<0.05]
        mask = np.isin(comparation_high_array, low_values_array)
        comparation_high_array=[~mask]
        difference_high_array.append(np.mean(comparation_high_array)-np.mean(low_values_array))

    most_skilled_case=np.argmin(np.array(difference_high_array))
    removed_high_elem=extreme_technique_array[most_skilled_case]

    print('The final most skilled case:')
    print(boxer_nationality_list[removed_high_elem])

    p_values_impartiality=[]
    for values in range(len(number_of_p)):   # loop to compare distributions with the most extreme imparciality
        try:
            _, pvalue=sp.stats.chisquare(np.array(p_value_matrix)[:,values], f_exp=np.array(p_value_matrix)[:,removed_elem])
            p_values_impartiality.append(pvalue)
        except:
            p_values_impartiality.append(0.0)
    
    p_values_technique=[]
    for values in range(len(number_of_p)):   # loop to compare distributions with the most extreme imparciality
        try:
            _, pvalue=sp.stats.chisquare(np.array(p_value_matrix)[:,values], f_exp=np.array(p_value_matrix)[:,removed_high_elem])
            p_values_technique.append(pvalue)
        except:
            p_values_technique.append(0.0)
    """plt.figure()
    plt.plot(boxer_nationality_list, p_values_impartiality, label='Most unjustly impartial case')
    plt.plot(boxer_nationality_list, p_values_technique, label='Most technical skilled case')
    plt.xlabel("Boxer's nationality")
    plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
    plt.ylabel('p-values')
    plt.savefig('upper_and_lower_impartial_bounds_panam.png', dpi=300, bbox_inches='tight')"""
    

    
    ###########################     OPTION 2    #################################################################
    """
    plt.figure()
    for i in extreme_imparciality_array:
        p_values_impartiality_2=[]
        for value in range(len(number_of_p)):
            try:
                _, pvalue=levene(np.array(p_value_matrix)[:,value], np.array(p_value_matrix)[:,i])
                p_values_impartiality_2.append(pvalue)
            except:
                p_values_impartiality_2.append(0.0)
        
        plt.plot(boxer_nationality_list, p_values_impartiality_2, label='Hypothesis testing with {}'.format(boxer_nationality_list[i]))
        plt.title('Most unjustly impartial cases')
        plt.xlabel("Boxer's nationality")
        plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
        plt.ylabel('p-values')
        plt.legend()
        plt.savefig('low_impartial_bounds_2.png', dpi=300, bbox_inches='tight')
    

    plt.figure()
    for i in extreme_technique_array:
        p_values_technique_2=[]
        for value in range(len(number_of_p)):
            try:
                _, pvalue=levene(np.array(p_value_matrix)[:,value], np.array(p_value_matrix)[:,i])
                p_values_technique_2.append(pvalue)
            except:
                p_values_technique_2.append(0.0)
        plt.plot(boxer_nationality_list, p_values_technique_2, label='Hypothesis testing with {}'.format(boxer_nationality_list[i]))
        plt.title('Most technical skilled cases')
        plt.xlabel("Boxer's nationality")
        plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
        plt.ylabel('p-values')
        plt.legend()
        plt.savefig('upper_impartial_bounds_2_p-values.png', dpi=300, bbox_inches='tight')

    
    
    ###########################     OPTION 3    #################################################################
    
    mean_values_array=[]
    variance_array=[]
    for j in range(num_columns):
        mean_values_array.append(np.mean(np.array(p_value_matrix)[:, j]))
        variance_array.append(np.var(np.array(p_value_matrix)[:, j]))

    array_order_elements=[i for i in range(len(boxer_nationality_list))]

    dict_values={}
    mean_dict={}
    variance_dict={}
    order_dict={}
    

    for i in range(len(boxer_nationality_list)):
        dict_values[boxer_nationality_list[i]]=number_of_p[i]
        mean_dict[boxer_nationality_list[i]]=mean_values_array[i]
        variance_dict[boxer_nationality_list[i]]=variance_array[i]
        order_dict[boxer_nationality_list[i]]=array_order_elements[i]

    sorted_dict = dict(sorted(dict_values.items(), key=lambda item: item[1]))
    
    boxer_sorted=list(sorted_dict.keys())
    pvalues_sorted=list(sorted_dict.values())

    ordered_keys = sorted_dict.keys()
    
    mean_sorted_dict = {key: mean_dict[key] for key in ordered_keys}
    variance_sorted_dict = {key: variance_dict[key] for key in ordered_keys}
    order_sorted_dict={key: order_dict[key] for key in ordered_keys}

    mean_sorted_array=list(mean_sorted_dict.values())
    variance_sorted_array=list(variance_sorted_dict.values())
    order_sorted_array=list(order_sorted_dict.values())

    counter=pvalues_sorted.count(0)

    plt.figure()
    plt.plot(boxer_sorted, mean_sorted_array)
    plt.vlines(boxer_sorted[counter], 0.2, 0.9, colors='black', linestyles='dotted')
    plt.xticks(range(len(boxer_sorted)), boxer_sorted, rotation=45, fontsize=5) 
    plt.title('Mean')
    plt.savefig('Mean_p-values.png')
    plt.figure()
    plt.plot(boxer_sorted, variance_sorted_array)
    plt.vlines(boxer_sorted[counter], 0, 0.125, colors='black', linestyles='dotted')
    plt.xticks(range(len(boxer_sorted)), boxer_sorted, rotation=45, fontsize=5) 
    plt.title('Variance')
    plt.savefig('Variance_p-values.png')

    sorted_matrix = p_value_matrix[:, order_sorted_array]

    
    statistical_difference_dict={}
    for j in range(len(order_sorted_array)):
        samples = [sorted_matrix[:, j]] + [sorted_matrix[:, i] for i in range(counter-1)]
        statistic, p_value=stats.kruskal(*samples, nan_policy='propagate', axis=0, keepdims=False)
        statistical_difference_dict[boxer_sorted[j]]=p_value

    with open('p_values.txt', 'w') as file:
        for key, value in statistical_difference_dict.items():
            file.write(f"{key}\t{value}\n")

    ###########################     OPTION 4    #################################################################

    mean_values_array=[]
    variance_array=[]
    for j in range(num_columns):
        mean_values_array.append(np.mean(np.array(result_matrix)[:, j]))
        variance_array.append(np.var(np.array(result_matrix)[:, j]))

    array_order_elements=[i for i in range(len(boxer_nationality_list))]

    dict_values={}
    mean_dict={}
    variance_dict={}
    order_dict={}
    

    for i in range(len(boxer_nationality_list)):
        dict_values[boxer_nationality_list[i]]=number_of_p[i]
        mean_dict[boxer_nationality_list[i]]=mean_values_array[i]
        variance_dict[boxer_nationality_list[i]]=variance_array[i]
        order_dict[boxer_nationality_list[i]]=array_order_elements[i]

    sorted_dict = dict(sorted(dict_values.items(), key=lambda item: item[1]))
    
    boxer_sorted=list(sorted_dict.keys())
    pvalues_sorted=list(sorted_dict.values())

    ordered_keys = sorted_dict.keys()
    
    mean_sorted_dict = {key: mean_dict[key] for key in ordered_keys}
    variance_sorted_dict = {key: variance_dict[key] for key in ordered_keys}
    order_sorted_dict={key: order_dict[key] for key in ordered_keys}

    mean_sorted_array=list(mean_sorted_dict.values())
    variance_sorted_array=list(variance_sorted_dict.values())
    order_sorted_array=list(order_sorted_dict.values())

    counter=pvalues_sorted.count(0)

    plt.figure()
    plt.plot(boxer_sorted, mean_sorted_array)
    plt.vlines(boxer_sorted[counter], -0.8, 0.5, colors='black', linestyles='dotted')
    plt.xticks(range(len(boxer_sorted)), boxer_sorted, rotation=45, fontsize=5) 
    plt.title('Mean')
    plt.savefig('Mean_values.png')
    plt.figure()
    plt.plot(boxer_sorted, variance_sorted_array)
    plt.vlines(boxer_sorted[counter], 0.1, 0.9, colors='black', linestyles='dotted')
    plt.xticks(range(len(boxer_sorted)), boxer_sorted, rotation=45, fontsize=5) 
    plt.title('Variance')
    plt.savefig('Variance_values.png')

    sorted_matrix = result_matrix[:, order_sorted_array]

    
    statistical_difference_dict={}
    for j in range(len(order_sorted_array)):
        samples = [sorted_matrix[:, j]] + [sorted_matrix[:, i] for i in range(counter-1)]
        statistic, p_value=stats.kruskal(*samples, nan_policy='propagate', axis=0, keepdims=False)
        statistical_difference_dict[boxer_sorted[j]]=p_value

    with open('values.txt', 'w') as file:
        for key, value in statistical_difference_dict.items():
            file.write(f"{key}\t{value}\n")"""

    
    #############################################################################################

    
    #############################################################################################

    

    combined_matrix=np.zeros_like(p_value_matrix)
    combined_matrix[p_value_matrix<0.05]=p_value_matrix[p_value_matrix<0.05]
    combined_matrix[p_value_matrix_low>-0.05]=p_value_matrix_low[p_value_matrix_low>-0.05]    

    combined_matrix[(combined_matrix>0) & (combined_matrix<0.05)]=0.5
    combined_matrix[(combined_matrix>-0.05) & (combined_matrix<0)]=-0.5
    

    plt.figure()
    plt.imshow(combined_matrix, cmap='bwr', interpolation='nearest')
    plt.xlabel("Boxer's nationality")
    plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
    plt.ylabel("Judge's nationality")
    plt.yticks(range(len(judge_nationality_list)), judge_nationality_list, rotation=45, fontsize=5) 
    #plt.show()
    plt.savefig('p-values matrix.png', dpi=300, bbox_inches='tight')
        

    
    """
    plt.figure()
    plt.bar(boxer_nationality_list, percentages, color='skyblue')
    plt.xlabel('Boxer nationalities')
    plt.ylabel('Percentage ')
    plt.xticks(rotation=45, fontsize=8) 
    plt.tight_layout()
    #plt.show()
    plt.savefig('percentage_p-values.png', dpi=300, bbox_inches='tight')

    plt.figure()
    plt.imshow(matrix_count_nationalities, cmap='viridis', interpolation='nearest')
    plt.title('Interactions Between Nationalities')
    plt.colorbar()  # To add a color bar indicating values
    plt.xlabel("Boxer's nationality")
    plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
    plt.ylabel("Judge's nationality")
    plt.yticks(range(len(judge_nationality_list)), judge_nationality_list, rotation=45, fontsize=5) 
    #plt.show()
    plt.savefig('nationality matrix.png', dpi=300, bbox_inches='tight')

    plt.figure()
    plt.imshow(result_matrix, cmap='viridis', interpolation='nearest')
    plt.title('Number of fights each ')
    plt.colorbar()  # To add a color bar indicating values
    plt.xlabel("Boxer's nationality")
    plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
    plt.ylabel("Judge's nationality")
    plt.yticks(range(len(judge_nationality_list)), judge_nationality_list, rotation=45, fontsize=5) 
    #plt.show()
    plt.savefig('normalized matrix.png', dpi=300, bbox_inches='tight')"""
               
nationalities_matrix()

def nationalities_matrix_panam():

    judge_nationality_dict={}
    boxer_nationality_dict={}

    # loop to create all the keys for boxer's nationality and judge's nationality
    for row_persona in results_persona_panam:
        if row_persona[-1]=='boxer':
            if row_persona[2] not in boxer_nationality_dict:
                boxer_nationality_dict[row_persona[2]]=0
        
        if row_persona[-1]=='judge':
            if row_persona[2] not in judge_nationality_dict:
                judge_nationality_dict[row_persona[2]]=0

    judge_nationality_list=list(judge_nationality_dict.keys())  
    boxer_nationality_list=list(boxer_nationality_dict.keys()) 

    # matrixes with the same number of rows as judge_nationality_list and same number of columns as boxer_nationality_list
    matrix_count_nationalities=[[0 for _ in range(len(boxer_nationality_list))] for _ in range(len(judge_nationality_list))]
    matrix_normalized_nationalities=[[0 for _ in range(len(boxer_nationality_list))] for _ in range(len(judge_nationality_list))]

    
    for row_matches in results_matches_panam:
        match_list=id_matches(row_matches) # [id, phase, id_boxer_red, id_boxer_blue, id_judge_1, id_judge_2, id_judge_3, id_judge_4, id_judge_5]
        nationality_judge=[]

        for row_persona in results_persona_panam: # obtain the nationality of the boxers and judges
                            
            if match_list[2]==row_persona[0]:
                nationality_red_boxer=row_persona[2] # red boxer
            elif match_list[3]==row_persona[0]:
                nationality_blue_boxer=row_persona[2] # blue boxer

            for i in range(4,9): # [id_judge_1, id_judge_2, id_judge_3, id_judge_4, id_judge_5]
                if match_list[i]==row_persona[0]:
                    nationality_judge.append(row_persona[2]) #list with the judges
            counter=0

        for row_points in results_points_panam: # look in the points table
            
            if row_points[2]==match_list[0]: # look for the fight
                if counter==0:
                    round_red=round_points(row_points)  # ['points_1', 'points_2', 'points_3'] red points list
                    counter=1
                    

                elif counter==1:
                    round_blue=round_points(row_points) # ['points_1', 'points_2', 'points_3'] blue points list

                    counter=0
                    difference_in_each_round = [x - y for x, y in zip(round_red, round_blue) if x is not None and y is not None]
                    

                    position_id = match_list.index(row_points[1])   # look for the judge in the match_list

                    nationality =nationality_judge[position_id-4]     # look for the nationality

                    i=judge_nationality_list.index(nationality)                 # index of the judge nationality in the whole list of judge nationalities
                    j_red=boxer_nationality_list.index(nationality_red_boxer)   # index of the red nationality in the whole list of judge nationalitie
                    j_blue=boxer_nationality_list.index(nationality_blue_boxer) # index of the blue nationality in the whole list of judge nationalitie

                    matrix_count_nationalities[i][j_red] +=3 # count of the rounds
                    matrix_count_nationalities[i][j_blue] +=3

                    matrix_normalized_nationalities[i][j_red] += np.sum(difference_in_each_round)
                    matrix_normalized_nationalities[i][j_blue] += -np.sum(difference_in_each_round)

    result_matrix = []

    # Normalization of the matrix
    for row1, row2 in zip(matrix_normalized_nationalities, matrix_count_nationalities):
        row_result = []
        for elem1, elem2 in zip(row1, row2):
            if elem2!=0:
                row_result.append(elem1 / elem2)
            else:
                row_result.append(0)
        result_matrix.append(row_result)


    result_matrix=np.array(result_matrix)

    num_permutations = 10000

    # Matrix of p-values
    
    dimensions = np.shape(result_matrix)
    rows_result_matrix, columns_result_matrix = dimensions
    
    p_value_matrix=np.empty((rows_result_matrix, columns_result_matrix))
    
    for j in range(rows_result_matrix): # loop over the rows
        # array with the same length as the rows to save the number of times the shuffled values are larger than the real one
        save_array=np.zeros(columns_result_matrix)     
                                            
        for i in range(num_permutations):
            row_shuffled=result_matrix[j,:]
            shuffle_completed=np.random.permutation(row_shuffled)
            for k in range(len(save_array)):
                if shuffle_completed[k]>=result_matrix[j,k]:
                    save_array[k]+=1
        p_value_array=[x/num_permutations for x in save_array]
        p_value_matrix[j, :] = p_value_array

    p_value_matrix_low=np.empty((rows_result_matrix, columns_result_matrix))

    result_matrix_low=-1*result_matrix
    
    for j in range(rows_result_matrix): 
        # array with the same length as the rows to save the number of times the shuffled values are larger than the real one
        save_array_low=np.zeros(columns_result_matrix)     
                                            
        for i in range(num_permutations):
            row_shuffled_low=result_matrix_low[j,:]
            shuffle_completed_low=np.random.permutation(row_shuffled_low)
            for k in range(len(save_array_low)):
                if shuffle_completed_low[k]>=result_matrix_low[j,k]:
                    save_array_low[k]+=1
        p_value_array_low=[x/num_permutations for x in save_array_low]
        p_value_matrix_low[j, :] = p_value_array_low
    
    p_value_matrix_low=-p_value_matrix_low 


    ###########################     OPTION 1    #################################################################
        
    num_columns = len(p_value_matrix[0])

    number_of_p=[]

    for j in range(num_columns):
        extreme_cases = np.array(p_value_matrix)[:, j]
        number_of_p.append(np.sum(extreme_cases <= 0.05)) # number of significant p-values in each column
    

    greater_p=max(number_of_p)
    extreme_technique_array=[i for i, n in enumerate(number_of_p) if n == greater_p]  # position of the columns with greater number of sig. p-values

    print('Most probable skilled countries PANAM:')
    print(len(extreme_technique_array))

    extreme_imparciality_array=[i for i, n in enumerate(number_of_p) if n == 1]   # position of the columns with just one sig. p-value
    print('Most probable unfair benefitiated countries PANAM:')
    print(len(extreme_imparciality_array))

    difference_array=[]

    for values in extreme_imparciality_array:     # loop to obtain the distribution with more diference between the significant p-value and the rest
        comparation_array=np.array(p_value_matrix)[:,values]
        low_value=min(comparation_array)
        comparation_array=comparation_array[comparation_array!=low_value]
        difference_array.append(np.mean(comparation_array)-low_value)

    worst_case=np.argmax(np.array(difference_array)) # position of the element with maximum difference in the extreme_imp. array
    removed_elem=extreme_imparciality_array[worst_case] # position of the element with maximum difference in number_of_p

    print('The final most unjust case PANAM:')
    print(boxer_nationality_list[removed_elem])

    difference_high_array=[]
    for values in extreme_technique_array:     # loop to obtain the distribution with more diference between the significant p-value and the rest
        comparation_high_array=np.array(p_value_matrix)[:,values]
        low_values_array=comparation_high_array[comparation_high_array<0.05]
        mask = np.isin(comparation_high_array, low_values_array)
        comparation_high_array=[~mask]
        difference_high_array.append(np.mean(comparation_high_array)-np.mean(low_values_array))

    most_skilled_case=np.argmin(np.array(difference_high_array))
    removed_high_elem=extreme_technique_array[most_skilled_case]

    print('The final most skilled case PANAM:')
    print(boxer_nationality_list[removed_high_elem])

    p_values_impartiality=[]
    for values in range(len(number_of_p)):   # loop to compare distributions with the most extreme imparciality
        try:
            _, pvalue=sp.stats.chisquare(np.array(p_value_matrix)[:,values], f_exp=np.array(p_value_matrix)[:,removed_elem])
            p_values_impartiality.append(pvalue)
        except:
            p_values_impartiality.append(0.0)
    
    p_values_technique=[]
    for values in range(len(number_of_p)):   # loop to compare distributions with the most extreme imparciality
        try:
            _, pvalue=sp.stats.chisquare(np.array(p_value_matrix)[:,values], f_exp=np.array(p_value_matrix)[:,removed_high_elem])
            p_values_technique.append(pvalue)
        except:
            p_values_technique.append(0.0)
    """plt.figure()
    plt.plot(boxer_nationality_list, p_values_impartiality, label='Most unjustly impartial case')
    plt.plot(boxer_nationality_list, p_values_technique, label='Most technical skilled case')
    plt.xlabel("Boxer's nationality")
    plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
    plt.ylabel('p-values')
    plt.savefig('upper_and_lower_impartial_bounds_panam.png', dpi=300, bbox_inches='tight')"""

        
        


    ###########################     OPTION 2    #################################################################

    """plt.figure()
    for i in extreme_imparciality_array:
        p_values_impartiality_2=[]
        for value in range(len(number_of_p)):
            try:
                _, pvalue=sp.stats.chisquare(np.array(p_value_matrix)[:,value], f_exp=np.array(p_value_matrix)[:,i])
                p_values_impartiality_2.append(pvalue)
            except:
                p_values_impartiality_2.append(0.0)
        
        plt.plot(boxer_nationality_list, p_values_impartiality_2, label='Hypothesis testing with {}'.format(boxer_nationality_list[i]))
        plt.title('Most unjustly impartial cases')
        plt.xlabel("Boxer's nationality")
        plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
        plt.ylabel('p-values')
        plt.legend()
        plt.savefig('low_impartial_bounds_2_panam.png', dpi=300, bbox_inches='tight')
    
    plt.figure()
    for i in extreme_technique_array:
        p_values_technique_2=[]
        for value in range(len(number_of_p)):
            try:
                _, pvalue=sp.stats.chisquare(np.array(p_value_matrix)[:,value], f_exp=np.array(p_value_matrix)[:,i])
                p_values_technique_2.append(pvalue)
            except:
                p_values_technique_2.append(0.0)
        plt.plot(boxer_nationality_list, p_values_technique_2, label='Hypothesis testing with {}'.format(boxer_nationality_list[i]))
        plt.title('Most technical skilled cases')
        plt.xlabel("Boxer's nationality")
        plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
        plt.ylabel('p-values')
        plt.legend()
        plt.savefig('upper_impartial_bounds_2_panam.png', dpi=300, bbox_inches='tight')"""
    
    

    
    #############################################################################################

    combined_matrix=np.zeros_like(p_value_matrix)
    combined_matrix[p_value_matrix<0.05]=p_value_matrix[p_value_matrix<0.05]
    combined_matrix[p_value_matrix_low>-0.05]=p_value_matrix_low[p_value_matrix_low>-0.05] 

    combined_matrix[(combined_matrix>0) & (combined_matrix<0.05)]=0.5
    combined_matrix[(combined_matrix>-0.05) & (combined_matrix<0)]=-0.5

    plt.figure()
    plt.imshow(combined_matrix, cmap='bwr', interpolation='nearest')
    plt.xlabel("Boxer's nationality")
    plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
    plt.ylabel("Judge's nationality")
    plt.yticks(range(len(judge_nationality_list)), judge_nationality_list, rotation=45, fontsize=5) 
    #plt.show()
    plt.savefig('p-values matrix_panam.png', dpi=300, bbox_inches='tight')

    """plt.figure()
    plt.imshow(matrix_count_nationalities, cmap='viridis', interpolation='nearest')
    plt.title('Interactions Between Nationalities')
    plt.colorbar()  # To add a color bar indicating values
    plt.xlabel("Boxer's nationality")
    plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
    plt.ylabel("Judge's nationality")
    plt.yticks(range(len(judge_nationality_list)), judge_nationality_list, rotation=45, fontsize=5) 
    #plt.show()
    plt.savefig('nationality matrix_panam.png', dpi=300, bbox_inches='tight')

    plt.figure()
    plt.imshow(result_matrix, cmap='viridis', interpolation='nearest')
    plt.title('Number of fights each ')
    plt.colorbar()  # To add a color bar indicating values
    plt.xlabel("Boxer's nationality")
    plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
    plt.ylabel("Judge's nationality")
    plt.yticks(range(len(judge_nationality_list)), judge_nationality_list, rotation=45, fontsize=5) 
    #plt.show()
    plt.savefig('normalized matrix_panam.png', dpi=300, bbox_inches='tight')"""
               
nationalities_matrix_panam()

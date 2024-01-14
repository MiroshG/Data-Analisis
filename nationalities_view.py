import mysql.connector
from collections import Counter
import numpy as np
from scipy.stats import chisquare
import scipy as sp
import matplotlib.pyplot as plt

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

# Close the connection
conn.close()

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

    num_permutations = 1000

    row_shuffled_p_values = np.zeros_like(result_matrix, dtype=float)
    column_shuffled_p_values = np.zeros_like(result_matrix, dtype=float)

    # Matrix of p-values
    for i in range(result_matrix.shape[0]):
        for j in range(result_matrix.shape[1]):
            element_values_row = result_matrix[i].copy()
            element_values_column = result_matrix[:, j].copy()
            
            row_shuffled_p_values_list = []
            column_shuffled_p_values_list = []
            
            for _ in range(num_permutations):
                np.random.shuffle(element_values_row)
                np.random.shuffle(element_values_column)
                
                # Calculate some statistic on shuffled row and column values (e.g., mean)
                row_shuffled_statistic = element_values_row #np.mean(element_values_row)
                column_shuffled_statistic = element_values_column #np.mean(element_values_column)
                
                # Calculate p-values based on the statistic of interest
                original_row_statistic = result_matrix[i, j]
                original_column_statistic = result_matrix[i, j]
                
                row_p_value = np.mean(row_shuffled_statistic > original_row_statistic)
                column_p_value = np.mean(column_shuffled_statistic > original_column_statistic)
                
                # Store the p-values
                row_shuffled_p_values_list.append(row_p_value)
                column_shuffled_p_values_list.append(column_p_value)
            
            # Assign the median p-value for robustness against outliers
            row_shuffled_p_values[i, j] = np.median(row_shuffled_p_values_list)
            column_shuffled_p_values[i, j] = np.median(column_shuffled_p_values_list)

    # Combine row and column shuffled p-values into a single p-value for each element
    combined_p_values = np.mean([row_shuffled_p_values, column_shuffled_p_values], axis=0)

    plt.figure()
    plt.imshow(combined_p_values, cmap='viridis', interpolation='nearest')
    plt.colorbar()  # To add a color bar indicating values
    plt.xlabel("Boxer's nationality")
    plt.xticks(range(len(boxer_nationality_list)), boxer_nationality_list, rotation=45, fontsize=5) 
    plt.ylabel("Judge's nationality")
    plt.yticks(range(len(judge_nationality_list)), judge_nationality_list, rotation=45, fontsize=5) 
    #plt.show()
    plt.savefig('p-values matrix.png', dpi=300, bbox_inches='tight')

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
    plt.savefig('normalized matrix.png', dpi=300, bbox_inches='tight')
               
nationalities_matrix()


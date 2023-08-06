
from itertools import combinations, product
import numpy as np
import pandas as pd
from copkmeans.cop_kmeans import cop_kmeans
import random





  
def make_random_choice(lst, links):
    new_list = []
    for x in range(links):
        choice = random.choice(lst)
        new_list.append(choice)
        if choice in new_list:
            lst.remove(choice)
    return new_list



def get_must_link(control_idx, covid_idx, links):
    control_comb = list(combinations(control_idx, 2))
    covid_comb = list(combinations(covid_idx, 2))
    
    must_link_control = make_random_choice(control_comb, links//2)
    must_link_covid = make_random_choice(covid_comb, links//2)

    return must_link_control + must_link_covid

  
def get_cannot_link(control_idx, covid_idx, links):
    covid_control_comb = list(product(covid_idx, control_idx))
    must_link_covid = make_random_choice(covid_control_comb, links)
    return must_link_covid



def get_constraints(df, links=20):

    control_idx = list(df[df['result'] == 'Control'].index)
    covid_idx = list(df[df['result'] == 'Covid'].index)

    must_link = get_must_link(control_idx, covid_idx, links)
    cannot_link = get_cannot_link(control_idx, covid_idx, links)
    
    return must_link, cannot_link



def get_clusters(df):

    must_link, cannot_link = get_constraints(df, 6)
    X = df.drop('result', axis=1)
    input_matrix = X.values
    clusters, centers = cop_kmeans(dataset=input_matrix, k=2, ml=must_link,cl=cannot_link)

    return clusters, centers
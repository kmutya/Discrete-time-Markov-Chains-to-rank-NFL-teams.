#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:33:19 2018

@author: Kartik
"""

import os
import pandas as pd
import numpy as np
import matplotlib as plt
from numpy.linalg import matrix_power

os.getcwd()
os.chdir('/Users/apple/Google Drive/A&M/Fall 2018/ISEN 609/assignment')
data = pd.read_csv('data_2007.csv')
data = data.rename(index = str, columns = {"Winner/tie": "Winner", "Loser/tie": "Loser"})
sum(data.PtsW == data.PtsL) #No ties???
data = data[0:256]


len(data.Winner.unique()) #32 teams
len(data.Loser.unique()) #32 teams

teams = np.sort(data.Winner.unique()) #all the 32 teams

#Max number of matches played

for i in teams:
    length = np.concatenate((data.loc[data.Winner == i, 'Loser'].values, 
                      data.loc[data.Loser == i, 'Winner'].values), axis = None)
    print('Matches played by', i, ':', len(length))
    

N = 16 #Max number of matches played

#df2 is the Transition Matrix
df2 = pd.DataFrame(np.random.randint(low=0, high=1, size=(32, 32)), columns=['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens',
       'Buffalo Bills', 'Carolina Panthers', 'Chicago Bears',
       'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys',
       'Denver Broncos', 'Detroit Lions', 'Green Bay Packers',
       'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars',
       'Kansas City Chiefs', 'Miami Dolphins', 'Minnesota Vikings',
       'New England Patriots', 'New Orleans Saints', 'New York Giants',
       'New York Jets', 'Oakland Raiders', 'Philadelphia Eagles',
       'Pittsburgh Steelers', 'San Diego Chargers', 'San Francisco 49ers',
       'Seattle Seahawks', 'St. Louis Rams', 'Tampa Bay Buccaneers',
       'Tennessee Titans', 'Washington Redskins'])
    
#Create a dictionary of teams with their state space
my_dict = {'Arizona Cardinals' : 0, 'Atlanta Falcons' : 1, 'Baltimore Ravens' : 2,
       'Buffalo Bills' : 3, 'Carolina Panthers' : 4, 'Chicago Bears' : 5,
       'Cincinnati Bengals' : 6, 'Cleveland Browns' : 7, 'Dallas Cowboys' : 8,
       'Denver Broncos' : 9, 'Detroit Lions' : 10, 'Green Bay Packers' : 11,
       'Houston Texans' : 12, 'Indianapolis Colts' : 13, 'Jacksonville Jaguars' : 14,
       'Kansas City Chiefs' : 15, 'Miami Dolphins' : 16, 'Minnesota Vikings' : 17,
       'New England Patriots' : 18, 'New Orleans Saints' : 19, 'New York Giants' : 20,
       'New York Jets' : 21, 'Oakland Raiders' : 22, 'Philadelphia Eagles' : 23,
       'Pittsburgh Steelers' : 24, 'San Diego Chargers' : 25, 'San Francisco 49ers' : 26,
       'Seattle Seahawks' : 27, 'St. Louis Rams' : 28, 'Tampa Bay Buccaneers' : 29,
       'Tennessee Titans' : 30, 'Washington Redskins' : 31}

#Function to create a transition matrix
p = 0.8 #arbitrary value selected
q = 0.2 #arbitrary value selected
def get_matrix(data_original, team, data_state, team_dict):
    '''Takes in the original dataframe, team, empty transition matrix and dictionary to give
    a transition matrix based on values of p and 1'''
    t1 = data_original.loc[data_original.Winner == team, 'Loser'].unique() #Teams supplied 'team' WON against 
    t2 = data_original.loc[data_original.Loser == team, 'Winner'].unique() #Teams suuplied 'team' LOST again
    t3 = np.intersect1d(t1,t2) #Teams supplied 'team' both won and lost against, p = 0.5 for this 
    t1 = np.setdiff1d(t1,t3) #Removing the intersection for WON 
    t2 = np.setdiff1d(t2,t3) #Removing the intersection for LOST
    for name, state in team_dict.items():
        if name == team:
            l = state #l is the state space number 
    for i in t1:
        data_state.loc[l, i] = q
    for j in t2:
        data_state.loc[l, j] = p
    for k in t3:
        data_state.loc[l, k] = 0.5
    return(data_state)
     
for i in teams:
    get_matrix(data, i, df2, my_dict)
            
row_sum = df2.sum(axis = 1).to_dict()
transition_mat = df2.values

            
final_mat  = transition_mat/transition_mat.sum(axis = 1)[:, None]
final_mat.sum(axis = 1) #All rows add up to 1

raised_mat = matrix_power(final_mat, 10000)
steady_state = dict(enumerate(raised_mat[1]))
#Sort dictionary by value
rank = sorted(steady_state, key = steady_state.get, reverse = True)

#Result
for r in rank:
    for name, state in my_dict.items():
        if r == state:
            print(name)



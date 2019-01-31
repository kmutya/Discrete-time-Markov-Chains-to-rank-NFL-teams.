#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 19:18:56 2018

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
data.Winner.isnull()#256 to 267 rows are null i.e Playoff rows
data = data[0:256]

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


data.loc[data.Winner == 'Arizona Cardinals', ['Winner','Loser', 'PtsL']] #Points conceded by teams against Arizona. Therefore team -> Arizona
data.loc[data.Loser == 'Arizona Cardinals', ['Winner','Loser', 'PtsL']] 

data2 = data[['Winner', 'Loser', 'PtsW', 'PtsL']]

############    
#Function to assign Loser -> Winner scores (L -> W, PtsW)
def L_W(data, my_dict, winner, data2):
    for loser in data.loc[data.Winner == winner, 'Loser'].unique():
        for team, value in my_dict.items():
            if loser == team:
                i = value
                l = sum(data.loc[(data.Loser == loser) & (data.Winner == winner), 'PtsW'].values)
                j = winner
                data2.loc[i, j] = l
    return(data2)

t1 = data[['Winner', 'Loser', 'PtsW']]
win_team = t1.Winner.unique()
for winner in win_team:
    L_W(t1, my_dict, winner, df2)
       
#Function to assign Winner -> Loser score (W -> L, PtsL)

def W_L(data, my_dict, winner, data2):
    for loser in data.loc[data.Winner == winner, 'Loser'].unique():
        for team, value in my_dict.items():
            if winner == team:
                i = value
                l = sum(data.loc[(data.Loser == loser) & (data.Winner == winner), 'PtsL'].values)
                j = loser
                data2.loc[i, j] = l
    return(data2)

t2 = data[['Winner', 'Loser', 'PtsL']]
for winner in win_team:
    W_L(t2, my_dict, winner, df2)


#Sum by row
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





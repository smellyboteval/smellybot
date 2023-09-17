#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 00:47:35 2022

@author: amal
"""


import time
import pandas as pd 
import Parse.Extractor as Extractor
from pathlib import Path
from multiprocessing import Pool
import glob


def extractFromProject (projname):
    
    
    all_classes = pd.DataFrame (columns = ['Project', 'File', 'Class', 'Class Code'])
    all_methods = pd.DataFrame (columns = ['Project', 'File', 'Method', 'Method Code'])    
    all_data = pd.DataFrame (columns = ['Project', 'File', 'Method','Method Code', 'Class', 'Class Code'])

    
    rootdir = projname
    #"""
    #pathlist = Path(rootdir).glob('**/*.java')
    pathlist = glob.glob('../**/*.java', recursive=True)
    path_in_str = list(map(str, pathlist))
    
    all_data['File'] = path_in_str
    all_data['Project'] = rootdir
    
    p = Pool(processes=10)
    results = p.imap(Extractor.Extract, path_in_str)

    
    df = pd.DataFrame(results, columns =['Method', 'Method Code', 'Class', 'Class Code'])  
    all_data['Method'].fillna(df['Method'], inplace=True)
    all_data['Method Code'].fillna(df['Method Code'], inplace=True)

    all_data['Class'].fillna(df['Class'], inplace=True)
    all_data['Class Code'].fillna(df['Class Code'], inplace=True)
    
    #print(all_data)
    #all_classes = all_data[['Project name', 'File path', 'Class']].explode('Class')
    #all_methods = all_data[['Project name', 'File path', 'Method']].explode('Method')    
    
    all_classes = all_data[['Project', 'File', 'Class','Class Code']].set_index(['Project', 'File']).apply(pd.Series.explode).reset_index()
    all_methods= all_data[['Project', 'File', 'Method', 'Method Code']].set_index(['Project', 'File']).apply(pd.Series.explode).reset_index()
    

    # Rename columns using the rename() function
    all_classes = all_classes.rename(columns={'Class Code': 'Code'})
    all_methods = all_methods.rename(columns={'Method Code': 'Code'})
    
    saveToFile(all_classes, 'classes', projname)
    saveToFile(all_methods, 'methods', projname)
    
       
def saveToFile (listOfObjs, typeOfObj, projname, mode='w', header=True): 
    listOfObjs.to_csv(projname.split('/')[-1]+ "_" +typeOfObj + ".csv",  mode=mode, header=header)
    
def check_if_file_exists(file_path):
    p = Path(file_path)
    print('________', p.with_suffix('.csv').exists())
    return p.with_suffix('.csv').exists()

if __name__ == "__main__":

    projname = 'data' #'Projects/'+project
    start_time = time.time()
    extractFromProject(projname)
        
    extract_time = round((time.time() - start_time))
    print(extract_time)
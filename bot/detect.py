#!/usr/bin/env python
# coding: utf-8

import requests
import os
import pandas as pd
import re
import time


#classes_file = os.path.join('data_classes.csv') #'bot\data_classes.csv'
#methods_file = os.path.join('data_methods.csv') 
classes_file = 'data_classes'
methods_file = 'data_methods'

url_dc= "https://detfe-dy5owqlgaq-ww.a.run.app" #"https://detdc-dy5owqlgaq-ww.a.run.app" 
url_gc= "https://detlm-dy5owqlgaq-ww.a.run.app" #"https://detgc-dy5owqlgaq-ww.a.run.app"
url_fe= "https://detfe-dy5owqlgaq-ww.a.run.app"
url_lm= "https://detlm-dy5owqlgaq-ww.a.run.app"


urls_file = {'DC': (url_dc, classes_file ), 
             'GC': (url_gc, classes_file), 
             'FE': (url_fe, methods_file), 
             'LM': (url_lm, methods_file)}



def get_results(url, file):

    resp = requests.post(url, files={'cfile': open(file, 'rb')})
    #print(resp.content)

    return resp


def save_report(reportdf, smellytype):

    # Convert DataFrame to Markdown table
    if smellytype == 'class':

        num_nonsmelly_dc = (reportdf['isDC'] == 0).sum()
        num_smelly_dc = (reportdf['isDC'] == 1).sum()
        num_nonsmelly_gc = (reportdf['isGC'] == 0).sum()
        num_smelly_gc = (reportdf['isGC'] == 1).sum()

        reportdf = reportdf.loc[(reportdf['isDC'] == 1) | (reportdf['isGC'] == 1)]
        markdown_table = reportdf[['File', 'Class', 'isDC', 'isGC']].to_markdown(index=False)

        # Save Markdown table with statistics to a txt file
        with open(smellytype + '_smelly_report.md', 'w') as f:
            f.write(f"Number of non-smelly classes (Data Class): {num_nonsmelly_dc}\n")
            f.write(f"Number of smelly classes (Data Class): {num_smelly_dc}\n")
            f.write(f"Number of non-smelly classes (God Class): {num_nonsmelly_gc}\n")
            f.write(f"Number of smelly classes (God Class): {num_smelly_gc}\n\n")
            if((num_smelly_dc+num_smelly_gc) > 0):
                reportdf.to_csv(smellytype + '_results.csv',  index=False)
                #f.write(markdown_table)

    elif smellytype == 'method':
        num_nonsmelly_fe = (reportdf['isFE'] == 0).sum()
        num_smelly_fe = (reportdf['isFE'] == 1).sum()
        num_nonsmelly_lm = (reportdf['isLM'] == 0).sum()
        num_smelly_lm = (reportdf['isLM'] == 1).sum()

        reportdf = reportdf.loc[(reportdf['isFE'] == 1) | (reportdf['isLM'] == 1)]
        markdown_table = reportdf[['File', 'Method', 'isFE', 'isLM']].to_markdown(index=False)

        # Save Markdown table with statistics to a txt filekk
        with open(smellytype + '_smelly_report.md', 'w') as f:
            f.write(f"Number of non-smelly methods (Feature Envy): {num_nonsmelly_fe}\n")
            f.write(f"Number of smelly methods (Feature Envy): {num_smelly_fe}\n")
            f.write(f"Number of non-smelly methods (Long Method): {num_nonsmelly_lm}\n")
            f.write(f"Number of smelly methods (Long Method): {num_smelly_lm}\n\n")
            if((num_smelly_fe+num_smelly_lm) > 0):
                reportdf.to_csv(smellytype + '_results.csv',  index=False)
                #f.write(markdown_table)



# Define a function to clean the code
def clean_code(code):
    cleaned_code = re.sub(r'[^a-zA-Z0-9+\-=()\[\];,<>{}*!&|\/~%^]', ' ', code)  # Replace non-letter characters with spaces
    cleaned_code = re.sub(r'\s+', ' ', cleaned_code)  # Replace multiple spaces with a single space
    return cleaned_code.strip()  # Remove leading and trailing spaces



def main():


    csv_directory = os.getcwd()
    classes_df = pd.DataFrame()
    methods_df = pd.DataFrame()

    for key in urls_file.keys():

        print(key, '->', urls_file[key])
        file = urls_file[key]
        url = urls_file[key][0]

        # Get a list of all CSV files in the directory
        csv_files = [filename for filename in os.listdir(csv_directory) if filename.startswith(file) and filename.endswith('.csv')]
        print(csv_files)

        # Loop through the list of CSV files
        for filename in csv_files:
            # Create the full file path
            file_path = os.path.join(csv_directory, filename)
            
            df = pd.read_csv(file_path)
            df['Code'] = df['Code'].apply(clean_code)
            
            resp = get_results(url, file_path)
            print(resp)
            result = resp.json()

            if key in ['DC', 'GC']:
                df['is'+ key] = list(result.values())[0]
                df['is'+ key] = df['is'+ key].astype(int) 
                classes_df = classes_df.append(df, ignore_index=True)
            elif key in ['FE', 'LM']:
                df['is'+ key] = list(result.values())[0]
                df['is'+ key] = df['is'+ key].astype(int)
                methods_df = methods_df.append(df, ignore_index=True)
            
            time.sleep(2)

    #print(classes_df)
    #print(methods_df)

    save_report(classes_df, 'class')
    save_report(methods_df, 'method')


if __name__ == "__main__":

    main()


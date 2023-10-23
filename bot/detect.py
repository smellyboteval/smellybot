#!/usr/bin/env python
# coding: utf-8

import requests
import os
import pandas as pd
import re
import time


#classes_file = os.path.join('data_classes.csv') #'bot\data_classes.csv'
#methods_file = os.path.join('data_methods.csv') 
classes_file = 'class'
methods_file = 'method'

url_dc= "https://detdc-dy5owqlgaq-ww.a.run.app" 
url_gc= "https://detgc-dy5owqlgaq-ww.a.run.app"
url_fe= "https://detfe-dy5owqlgaq-ww.a.run.app"
url_lm= "https://detlm-dy5owqlgaq-ww.a.run.app"


urls_file_class = {'DC': (url_dc, classes_file ), 
             'GC': (url_gc, classes_file) }

urls_file_method = { 'FE': (url_fe, methods_file), 
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
        #with open(smellytype + '_smelly_report.md', 'w') as f:
        #    f.write(f"Number of non-smelly classes (Data Class): {num_nonsmelly_dc}\n")
        #    f.write(f"Number of smelly classes (Data Class): {num_smelly_dc}\n")
        #    f.write(f"Number of non-smelly classes (God Class): {num_nonsmelly_gc}\n")
        #    f.write(f"Number of smelly classes (God Class): {num_smelly_gc}\n\n")
        if((num_smelly_dc+num_smelly_gc) > 0):
            reportdf.to_csv('Smellybot_report_' + smellytype + '_level.csv',  index=False)
                #f.write(markdown_table)

    elif smellytype == 'method':
        num_nonsmelly_fe = (reportdf['isFE'] == 0).sum()
        num_smelly_fe = (reportdf['isFE'] == 1).sum()
        num_nonsmelly_lm = (reportdf['isLM'] == 0).sum()
        num_smelly_lm = (reportdf['isLM'] == 1).sum()

        reportdf = reportdf.loc[(reportdf['isFE'] == 1) | (reportdf['isLM'] == 1)]
        markdown_table = reportdf[['File', 'Method', 'isFE', 'isLM']].to_markdown(index=False)

        # Save Markdown table with statistics to a txt file
        #with open(smellytype + '_smelly_report.md', 'w') as f:
        #    f.write(f"Number of non-smelly methods (Feature Envy): {num_nonsmelly_fe}\n")
        #    f.write(f"Number of smelly methods (Feature Envy): {num_smelly_fe}\n")
        #    f.write(f"Number of non-smelly methods (Long Method): {num_nonsmelly_lm}\n")
        #    f.write(f"Number of smelly methods (Long Method): {num_smelly_lm}\n\n")
        if((num_smelly_fe+num_smelly_lm) > 0):
            reportdf.to_csv('Smellybot_report_' + smellytype + '_level.csv',  index=False)
                #f.write(markdown_table)


def create_summary_report(class_report, method_report):

    num_nonsmelly_dc = (class_report['isDC'] == 0).sum()
    num_smelly_dc = (class_report['isDC'] == 1).sum()
    num_nonsmelly_gc = (class_report['isGC'] == 0).sum()
    num_smelly_gc = (class_report['isGC'] == 1).sum()

    num_nonsmelly_fe = (method_report['isFE'] == 0).sum()
    num_smelly_fe = (method_report['isFE'] == 1).sum()
    num_nonsmelly_lm = (method_report['isLM'] == 0).sum()
    num_smelly_lm = (method_report['isLM'] == 1).sum()
    
    # Create a summary report DataFrame
    data = {
        'Code Smell Type': ['Data Class', 'God Class', 'Feature Envy', 'Long Method'],
        'Smelly': [num_smelly_dc, num_smelly_gc, num_smelly_fe, num_smelly_lm],
        'Non-Smelly': [num_nonsmelly_dc, num_nonsmelly_gc, num_nonsmelly_fe, num_nonsmelly_lm]
    }

    summary_report = pd.DataFrame(data)

    # Save the summary report as a Markdown file
    with open('summary_report.md', 'w') as f:
        f.write(summary_report.to_markdown(index=False))



# Define a function to clean the code hjgh
def clean_code(code):
    cleaned_code = re.sub(r'[^a-zA-Z0-9+\-=()\[\];,<>{}*!&|\/~%^]', ' ', code)  # Replace non-letter characters with spaces
    cleaned_code = re.sub(r'\s+', ' ', cleaned_code)  # Replace multiple spaces with a single space
    return cleaned_code.strip()  # Remove leading and trailing spaces


def detect_classes(df, file_path):

    for key in urls_file_class.keys():

        print(key, '->', urls_file_class[key])
        level = urls_file_class[key]
        url = urls_file_class[key][0]

        print(level, url)
        resp = get_results(url, file_path)
        print(resp)
        result = resp.json()
        
        df['is'+ key] = list(result.values())[0]
        df['is'+ key] = df['is'+ key].astype(int) 

    return df

def detect_methods(df, file_path):

    for key in urls_file_method.keys():

        print(key, '->', urls_file_method[key])
        level = urls_file_method[key]
        url = urls_file_method[key][0]

        print(level, url)
        resp = get_results(url, file_path)
        print(resp)
        result = resp.json()

        df['is'+ key] = list(result.values())[0]
        df['is'+ key] = df['is'+ key].astype(int)

    return df

def main():
  
    classes_df = pd.DataFrame()
    methods_df = pd.DataFrame()

    # Get a list of all CSV files in the directory
    csv_directory = os.getcwd()
    csv_files = [filename for filename in os.listdir(csv_directory) if filename.startswith('data') and filename.endswith('.csv')]
    print(csv_files)

    # Loop through the list of CSV files
    for filename in csv_files:
        print(filename)
        # Create the full file path
        file_path = os.path.join(csv_directory, filename)
        
        df = pd.read_csv(file_path)
        df['Code'] = df['Code'].apply(clean_code)

        if 'classes' in filename:
            c_df = detect_classes(df, file_path)
            classes_df = classes_df.append(c_df, ignore_index=True)
        elif 'methods' in filename: 
            m_df = detect_methods(df, file_path)
            methods_df = methods_df.append(m_df, ignore_index=True)

            time.sleep(2)

        print(classes_df)
        print(methods_df)

    save_report(classes_df[['File', 'Class', 'isDC', 'isGC']], 'class')
    save_report(methods_df[['File', 'Method', 'isFE', 'isLM']], 'method')
    create_summary_report(classes_df[['File', 'Class', 'isDC', 'isGC']], methods_df[['File', 'Method', 'isFE', 'isLM']])


if __name__ == "__main__":

    main()


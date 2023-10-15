#!/usr/bin/env python
# coding: utf-8

import requests
import os
import pandas as pd
import re
import time


classes_file = os.path.join('data_classes.csv') #'bot\data_classes.csv'


url_dc= "https://detdc-dy5owqlgaq-ww.a.run.app" 
url_gc= "https://detgc-dy5owqlgaq-ww.a.run.app"



urls_file = {'DC': (url_dc, classes_file ), 
             'GC': (url_gc, classes_file), }



def get_results(url_file):

    resp = requests.post(url_file[0], files={'cfile': open(url_file[1] , 'rb')})
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
                f.write(markdown_table)



# Define a function to clean the code
def clean_code(code):
    cleaned_code = re.sub(r'[^a-zA-Z0-9+\-=()\[\];,<>{}*!&|\/~%^]', ' ', code)  # Replace non-letter characters with spaces
    cleaned_code = re.sub(r'\s+', ' ', cleaned_code)  # Replace multiple spaces with a single space
    return cleaned_code.strip()  # Remove leading and trailing spaces



def main():

    classes_df = pd.read_csv(classes_file)

    # Apply the cleaning function to the 'code' column
    classes_df['Code'] = classes_df['Code'].apply(clean_code)


    for key in urls_file.keys():

        print(key, '->', urls_file[key])
        cs = urls_file[key]
        resp = get_results(cs)

        print(resp)
        result = resp.json()
        if key in ['DC', 'GC']:
            classes_df['is'+ key] = list(result.values())[0]
            classes_df['is'+ key] = classes_df['is'+ key].astype(int) 

        time.sleep(2)

    
    save_report(classes_df, 'class')



if __name__ == "__main__":
    main()


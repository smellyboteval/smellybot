#!/usr/bin/env python
# coding: utf-8

import requests
import os
import pandas as pd
import re
import time



methods_file = os.path.join('data_methods.csv') 


url_fe= "https://detfe-dy5owqlgaq-ww.a.run.app"
url_lm= "https://detlm-dy5owqlgaq-ww.a.run.app"


urls_file = {'FE': (url_fe, methods_file), 
             'LM': (url_lm, methods_file)}



def get_results(url_file):

    resp = requests.post(url_file[0], files={'cfile': open(url_file[1] , 'rb')})
    #print(resp.content)

    return resp


def save_report(reportdf, smellytype):


    if smellytype == 'method':
        num_nonsmelly_fe = (reportdf['isFE'] == 0).sum()
        num_smelly_fe = (reportdf['isFE'] == 1).sum()
        num_nonsmelly_lm = (reportdf['isLM'] == 0).sum()
        num_smelly_lm = (reportdf['isLM'] == 1).sum()

        reportdf = reportdf.loc[(reportdf['isFE'] == 1) | (reportdf['isLM'] == 1)]
        markdown_table = reportdf[['File', 'Method', 'isFE', 'isLM']].to_markdown(index=False)

        # Save Markdown table with statistics to a txt file
        with open(smellytype + '_smelly_report.md', 'w') as f:
            f.write(f"Number of non-smelly methods (Feature Envy): {num_nonsmelly_fe}\n")
            f.write(f"Number of smelly methods (Feature Envy): {num_smelly_fe}\n")
            f.write(f"Number of non-smelly methods (Long Method): {num_nonsmelly_lm}\n")
            f.write(f"Number of smelly methods (Long Method): {num_smelly_lm}\n\n")
            if((num_smelly_fe+num_smelly_lm) > 0):
                f.write(markdown_table)



# Define a function to clean the code
def clean_code(code):
    cleaned_code = re.sub(r'[^a-zA-Z0-9+\-=()\[\];,<>{}*!&|\/~%^]', ' ', code)  # Replace non-letter characters with spaces
    cleaned_code = re.sub(r'\s+', ' ', cleaned_code)  # Replace multiple spaces with a single space
    return cleaned_code.strip()  # Remove leading and trailing spaces



def main():

    methods_df = pd.read_csv(methods_file)

    methods_df['Code'] = methods_df['Code'].apply(clean_code)


    for key in urls_file.keys():

        print(key, '->', urls_file[key])
        cs = urls_file[key]
        resp = get_results(cs)

        print(resp)
        result = resp.json()

        if key in ['FE', 'LM']:
            methods_df['is'+ key] = list(result.values())[0]
            methods_df['is'+ key] = methods_df['is'+ key].astype(int) 

        time.sleep(2)


    save_report(methods_df, 'method')



if __name__ == "__main__":
    main()


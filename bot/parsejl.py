import os
import time
import pandas as pd
from pathlib import Path
from multiprocessing import Pool
import Parse.javalangeparser as Extractor
from concurrent.futures import ThreadPoolExecutor
import re
import glob

def clean_path(input_path): 

    input_path = input_path.replace(".java", "\/")
    input_path = input_path.replace("..", "")
    input_path = input_path.replace(".", "-")
    input_path = input_path.replace("\/", ".", 2)

    # Define a regular expression pattern to remove the first two backslashes and replace the rest with dots
    pattern = r"[^.]+\/"

    # Use re.search to find the matched pattern in the input string
    match = re.search(pattern, input_path)

    if match:
        # Extract the matched portion
        output_string = match.group(0)
        output_string = output_string[:-1].replace("\/", ".")
        #print(output_string)
    else:
        print("Pattern not found in the input string.")
        output_string = ""

    return output_string

def clean_code(source_code):
    try:
    
      # Regular expression to remove single-line comments
      source_code = re.sub(r'//.*?\n', '\n', source_code)

      # Regular expression to remove multi-line comments
      source_code = re.sub(r'/\*.*?\*/', '', source_code, flags=re.DOTALL)

      # Remove multiple spaces 
      source_code = re.sub(r'\s+', ' ', source_code)

    except:
       source_code = ''

    return source_code

def get_class_name(c_code):

    try:
      result1 = re.search(r'(((|public|final|abstract|private|static|protected)(\s+))?(class|enum|interface)(\s+)(\w+)(<.*>)?(\s+extends\s+\w+)?(<.*>)?(\s+implements\s+)?(.*)?(<.*>)?(\s*))\{', c_code)

      # Extract match value of group 7
      cname = result1.group(7)
      #cname = cname.lower()
				
    # if code is nan
    except:
      cname = '' 
      
    return cname

def get_method_name(m_code):

    try:
      result = re.search(r'(public|protected|private|static|void|synchronized|String|byte|List|\s) *[\w\<\>\[\].#$]+\s+([$\w]+) *\([^\)]*\)? *(\{?|[^;])', m_code)
      # Extract match value of group 1
      mname = result.group(2)

    # if code is nan
    except:
      mname = ''  
      
    try:
      result = re.search(r'(([\w\<\>\[\].#$])+([$\w]*))\(', mname)
      mname = result.group(1)		
    except:
      mname = mname  

    return mname

def extractFromProject(projname, _extclass=True, _extrmethod=True):
    all_classes = pd.DataFrame (columns = ['Project', 'File', 'Class', 'Class Code'])
    all_methods = pd.DataFrame (columns = ['Project', 'File', 'Method', 'Method Code'])    
    all_data = pd.DataFrame (columns = ['Project', 'File', 'Method','Method Code', 'Class', 'Class Code'])

    rootdir = projname
    pathlist = glob.glob('../**/*.java', recursive=True)
    path_in_str = list(map(str, pathlist))
    #pathlist = Path(projname).glob('**/*.java')
    #path_in_str = list(map(str, pathlist))
    
    all_data['File'] = path_in_str
    all_data['Project'] = rootdir

    results = list(map(Extractor.Extract, path_in_str))
    
    df = pd.DataFrame(results, columns =['Method Code', 'Class Code'])  
    all_data['Method Code'].fillna(df['Method Code'], inplace=True)
    all_data['Class Code'].fillna(df['Class Code'], inplace=True)
    
    
    all_classes = all_data[['Project', 'File', 'Class Code']].set_index(['Project', 'File']).apply(pd.Series.explode).reset_index()
    all_methods= all_data[['Project', 'File', 'Method Code']].set_index(['Project', 'File']).apply(pd.Series.explode).reset_index()
    
    all_classes['Class'] = all_classes['Class Code'].apply(get_class_name)
    all_methods['Method'] = all_methods['Method Code'].apply(get_method_name)
    
    all_classes['Class Code'] = all_classes['Class Code'].apply(clean_code)
    all_methods['Method Code'] = all_methods['Method Code'].apply(clean_code)

    all_classes['File'] = all_classes['File'].apply(clean_path)
    all_methods['File'] = all_methods['File'].apply(clean_path)

    print(all_classes['File'])
    all_classes = all_classes.rename(columns={'Class Code': 'Code'})
    all_methods = all_methods.rename(columns={'Method Code': 'Code'})

    saveToFile(all_classes[['Project', 'File', 'Class', 'Code']], 'classes', projname)
    saveToFile(all_methods[['Project', 'File', 'Method', 'Code']], 'methods', projname)

# def saveToFile(listOfObjs, typeOfObj, projname):
    #file_name = f'{projname}_{typeOfObj}.csv'
    #listOfObjs.to_csv(file_name, index=False)

def saveToFile (listOfObjs, typeOfObj, projname, mode='w', header=True): 
    #listOfObjs = listOfObjs.dropna()
    listOfObjs.to_csv(projname.split('/')[-1]+ "_" +typeOfObj + ".csv",  mode=mode, header=header)

if __name__ == "__main__":
    projname = 'data' ## change to data in bot
    start_time = time.time()
    extractFromProject(projname)
    print('\t\tTime (seconds): ', round((time.time() - start_time)))

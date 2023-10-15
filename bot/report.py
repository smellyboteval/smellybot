import requests
import sys

import logging
import logging.handlers
import pandas as pd


def create_issue(url, payload, headers):
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Comment posted successfully!")
    else:
        print("Failed to post comment. Status Code:", response.status_code)
        print("Response Content:", response.text)
        print("Response Headers:", response.headers)


def issue_data(smellytype):

    # Read content from report.md
    with open(smellytype+'_smelly_report.md', 'r') as f:
        report = f.read()

    # Issue data
    table_content = f'{report}'
    issue_title = 'Code smells - '+smellytype
    comment = f"This is an automated comment.\n\n{table_content}"
    payload = {"title": issue_title, "body": comment}

    return payload


def main():
    repo =  sys.argv[1] 
    token = sys.argv[2]  # token uilyu yutdyu

    # Create a new issue
    url = f"https://api.github.com/repos/{repo}/issues"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload_class = issue_data('class')
    create_issue(url, payload_class, headers)
    #try:
    #    csv_file_path = 'class_results.csv'
    #    files={'csv_attachment': (csv_file_path, open(csv_file_path, 'rb'))}
    #except:
    #    files=None
    #create_issue(url, payload_class, headers, files=files )

    payload_method = issue_data('method')
    create_issue(url, payload_method, headers)
    #try:
    #    csv_file_path = 'method_results.csv'
    #    files={'csv_attachment': (csv_file_path, open(csv_file_path, 'rb'))}
    #except:
    #    files=None
    #create_issue(url, payload_method, headers, files=files )


    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        "smelly_classes.log",
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)

    # Read the CSV file fghn
    csv_file = 'class_results.csv'
    try:
        df = pd.read_csv(csv_file)
        rows = df.iterrows()  # Iterate over rows

        for index, row in rows:
            logger.info(f'Row {index}: {row}')
    except FileNotFoundError:
        logger.error(f"File '{csv_file}' not found.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")



if __name__ == "__main__":
    main()
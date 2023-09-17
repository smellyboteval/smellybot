import requests
import sys


def create_issue(url, payload, headers):
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Comment posted successfully!")
    else:
        print("Failed to post comment.")


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
    payload_method = issue_data('method')
    create_issue(url, payload_method, headers)


if __name__ == "__main__":
    main()
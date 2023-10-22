# Smellybot

### Step1 A: Install the bot
1. Fork the [Smellybot](https://github.com/amalazba/smellybot) repository to your account
2. Install the Github app named Smelly-Bot into the forked repository (ONLY) from [here](https://github.com/apps/smelly-bot)
3. Add two Actions secrets APP_ID and APP_PRIVATE_KEY, use the values in secrets.txt file: repo Settings >> Secrets and variables >> actions >> New repository secret
4. Make sure the Issues tap is available, to enable: repo Settings >> General >> Features >> issues
5. Enable GitHub Actions: Go to Actions tap >> click on "I understand my workflows, go ahead and enable them"

### Step1 B: Use the bot
1. Login to the evaluation account (the username and password will be given to you)
2. Creat a new branch by your name or neckname
    1. Click on branches
    ![Screenshot](figs/branches.PNG)

    2. Create new branch (use your name or nickname)
    ![Screenshot](figs/new_branch.PNG)

### Step2: Add a project to the fork/branch repository 
- A. Add your Java project or download a sample project from [here](https://github.com/amalazba/src-test)
    1. Make sure you select the branch you created 
    ![Screenshot](figs/select_branch.PNG)

    2. Click Add file >> Upload files
    ![Screenshot](figs/upload_files.PNG)

    3. Commit the changes to your branch
    ![Screenshot](figs/commit.PNG)


- B. From CMD:
    1. `git add .`
    2. `git commit -m 'add a comment'`
    3. `git push`

### Step3: View reports and issues
1. Refresh the page, check any new files
2. Go to Issues tap and view created issues
3. Go to Actions tap and view the status of the workflow
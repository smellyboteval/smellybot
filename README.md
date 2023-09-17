# smellybot
to edit:
open cmd
code .

to use:
must creat a PAT settings>>developers ettings>>personal access tokens , then create a new token
Add the created token into secrits as a secrit key with 'API_TOKEN'


to use as bot:
1- Creat Github app: https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app
2- Add APP_ID ans PRIVATE_KEY into ctions secrits 
3- Install app in the desired repository 
3- Use it to generate API tokens: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow



git add .
git commit -m 'bot in folder'
git push


----
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:amalazba/smellybot.git
git push -u origin main
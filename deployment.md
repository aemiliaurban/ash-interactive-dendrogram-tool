The app is deployed via Heroku.
Below is the link to the app:

[https://ash-clustering-80f7adc27a4c.herokuapp.com/](https://ash-clustering-80f7adc27a4c.herokuapp.com/)

What ought to be run is specified in the `Procfile`:
```
web: gunicorn app:server
```
You need to have Heroku CLI installed on your machine. Use homebrew to install it:
```
brew tap heroku/brew && brew install heroku
```

To deploy the app, you need to log in to Heroku:
```
heroku login
```
Then you have to set up heroku git remote:
```
heroku git:remote -a ash-clustering
```
Finally, you can deploy the app by simply pushing the code to the heroku remote:
```bash
git push heroku main
```

You can also deploy from other branches:
```bash
git push heroku your-branch:main
```

If you want to see the logs, you can use the following command:
```bash
heroku logs --tail
```
If you want to log to the console, you can use the following command:
```bash
heroku run bash
```





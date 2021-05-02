### Dependencies

Assuming pip is installed, run `pip install -r requirements.txt`

### Variables

* Update `DIALOGFLOW_PROJECT_ID` and `GOOGLE_SERVICE_ACCOUNT_FILE_PATH`.  The latter shoud point to the location of the service account key file in this repo.
* Update `TELEGRAM_API_TOKEN` to receive feedback, and `TELEGRAM_USER_ID` to forward feedback to user.
* Pass these as environment variables. 

### Deployment

`export FLASK_APP=main.py && python -m flask run --port=9000`
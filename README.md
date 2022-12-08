To set up and start the server you must
- pip install -r requirements.txt
- uvicorn main:app --reload 

You can either import your own "auths.json" with the following format:

{
    "lambda_user_auth": 0,
    "admin_auth": 1,
    "master_auth": 2,
    "another_master_auth": 2
}

If no auths.json is used, the server will create empty json file.

All routes can be seen on http://127.0.0.1:8000/docs or http://127.0.0.1:8000/openapi.json
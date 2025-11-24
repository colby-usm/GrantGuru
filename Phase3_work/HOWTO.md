# Overview
You need two terminal sessions:
T1: To run the web application
T2: To Run the Flask Session

Note, this will eventually be combined into 1 python script in 1 terminal.  For now, it is nice to have these in two terminals for debugging and feature development.


# 1. Setup NPM terminal (T1)
1. Create a python venv or conda env with python 3.12
2. cd GrantGuru:
3. install requirements.txt to your venv
4. nvm install 23.11.0
5. nvm use 23.11.0
6. cd Phase3_work/UI
7. npm install
8. npm run dev

# 2. Setup Flask Terminal (T2)
1. Launch a second terminnal for the flask process
2. Load a the python virtural environment
3. export FLASK_APP=api/auth/routes.py
4. cd Phase3_work/UI
5. flask run --host=127.0.0.1 --port=5000


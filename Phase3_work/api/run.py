# run.py
'''
    Author: Colby Wirth
    Veresion: 8 December 2025
    Description:
        Runs the backend on 127.0.0.1:5000
'''
from api import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

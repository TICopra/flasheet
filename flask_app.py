
# # A very simple Flask Hello World app for you to get started with...

# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello from Flask!'

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

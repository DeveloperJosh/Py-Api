from flask import session
from main import app

if __name__ == '__main__':
    app.config["SESSION_PERMANENT"] = False
    app.secret_key = 'HFIUDHGFYGHWEUYFGUYGFHDSGUIYFGWERUYG'
    app.config['SESSION_TYPE'] = 'filesystem'
    session(app)
    app.run()
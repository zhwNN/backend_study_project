from flask import Flask
from tasks import tasks_bp
from db import init_database



app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(tasks_bp)

if __name__ == "__main__":
    init_database()
    app.run(debug=True)
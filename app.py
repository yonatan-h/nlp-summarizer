from flask import Flask, request
from summarize import summarize_bp 

app = Flask(__name__)
app.register_blueprint(summarize_bp)
if __name__ == '__main__':
    app.run()

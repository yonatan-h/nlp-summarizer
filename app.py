from flask import Flask, request
from summarize import summarize_bp 
import os

app = Flask(__name__)
app.register_blueprint(summarize_bp)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('my Running on port', port, flush=True)
    app.run(port=port, host="0.0.0.0")

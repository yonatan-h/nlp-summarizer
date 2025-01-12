from flask import Flask, request
from .main import handle_summary

app = Flask(__name__)

@app.route('/')
def introduce():
    return """
    Hello!
    Please use POST /summarize with {"text":"<several paragraphs>"}
    The response would be {"summary":"<summary>"}
    """

@app.post('/')
def summarize():
    json = request.json
    if not json:
        return {"error":"the summarize request doesn't contain a body"}, 400

    text = json.get('text')
    if not text:
        return {"error":"the summarize request doesn't contain 'text'"}, 400

    return {"summary":handle_summary(text)}
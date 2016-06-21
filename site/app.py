"""
Flask App
"""
from flask import Flask
from flask import request
from flask import render_template
from Knowledge_search import get_neighbors

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    result_list = get_neighbors.Network(text).child_articles
    return "\n".join(result_list)

if __name__ == '__main__':
    app.run()



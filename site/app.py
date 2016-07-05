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
    return render_template("new.html")

@app.route('/', methods=['POST'])
def my_form_post():
    title = request.form['title']
    node = get_neighbors.Network(title)
    parent = node.parent_article[0]
    comprable = ", ".join([article[0] for article in node.comprable_articles])
    #return node.child_articles[0][0]
    children = ", ".join([article[0] for article in node.child_articles])
    return render_template("response.html", article=node.article, parent=parent,
            comprable=comprable, children=children)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)



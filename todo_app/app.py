from flask import Flask, render_template, request

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html', items=get_items())


@app.route('/items', methods=['POST'])
def create():
    title = request.form.get('title')
    add_item(title)
    return render_template('index.html', items=get_items())


if __name__ == '__main__':
    app.run()

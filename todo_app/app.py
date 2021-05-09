from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config
from todo_app.trello_client import get_cards_from_board_items, create_card_on_todo_list, move_card_to_done_list

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html', items=get_cards_from_board_items())

@app.route('/items', methods=['POST'])
def create():
    title = request.form.get('title')
    create_card_on_todo_list(title)
    return redirect("/", code=303)

@app.route('/items/update', methods=['POST'])
def update():
    move_card_to_done_list(request.form.get('id'))
    return redirect("/", code=303)

if __name__ == '__main__':
    app.run()

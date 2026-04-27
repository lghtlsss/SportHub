from flask import Flask, render_template
from flask_login import login_required, logout_user, current_user

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title='Главная')


@app.route('/profile')
def profile():
    return


@app.route('/subscriptions')
def subscriptions():
    return


def main():
    app.run(port=8080, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()

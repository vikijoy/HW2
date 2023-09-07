from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        mail = session['mail']
        return render_template('index.html', username=username, mail=mail)
    else:
        return redirect(url_for('login'))


@app.route('/clothes/')
def clothes():
    _goods = [
        {
            "name": "Shoes",
            "price": 3000,
            "description": 'Shoes for running',
        },
        {
            "name": "Jacket",
            "price": 5000,
            "description": 'Stylish jacket',
        },
        {
            "name": "Pants",
            "price": 3500,
            "description": 'Your body feel nice in these pants',
        },
    ]
    return render_template('clothes.html', content=_goods)


@app.route('/games/')
def games():
    _games_data = [
        {
            "name": "Dune: the Battle for Arrakis",
            "price": 150,
            "description": '''A long time ago in a galaxy far far away... There was a dune ''',
        },
        {
            "name": "Counter-Strike 2",
            "price": 2000,
            "description": '''Eliminate terrorists, defuse the bomb, save the hostages... or do the opposite.''',
        },
        {
            "name": "Half-Life",
            "price": 1500,
            "description": '''Zombies, anomalies, Gordon Freeman. Perfect gameplay, without a word.'''}
    ]
    return render_template('games.html', content=_games_data)


@app.get('/login/')
def checker_get():
    return render_template('login.html')


@app.post('/login/')
def login():
    if request.method == 'POST':
        if not request.form['username']:
            flash('Ошибка, забыли ввести имя !', 'danger')
            return redirect(url_for('login'))
        if not request.form['mail']:
            flash('Ошибка, забыли ввести почту !', 'danger')
            return redirect(url_for('login'))
        # session
        session['username'] = escape(request.form.get('username'))
        session['mail'] = escape(request.form.get('mail'))
        # Cookie
        response = make_response(render_template('index.html', username=session['username'], mail=session['mail']))
        response.set_cookie('username', session['username'])
        response.set_cookie('mail', session['mail'])
        return response


@app.route('/logout/')
def logout():
    session.pop('username', None)
    session.pop('mail', None)
    print(f'(Exit) username: {request.cookies.get("username")}')
    print(f'mail: {request.cookies.get("mail")}')
    response = make_response(render_template('login.html'))
    response.delete_cookie("username")
    response.delete_cookie("mail")
    return response


@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning(e)
    context = {
        'title': 'Страница не найдена',
        'url': request.base_url,
    }
    return render_template('404.html', **context), 404


if __name__ == '__main__':
    app.run(debug=True)

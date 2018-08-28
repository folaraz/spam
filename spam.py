from flask import Flask, request, session
from core import predict
from flask_bootstrap import Bootstrap
from flask import url_for, redirect, render_template
from dir import get_full_path
import nltk

app = Flask(__name__)

bootstrap = Bootstrap(app)


app.config['SECRET_KEY'] = 'hard to guess string'

ALLOWED_EXTENSIONS = ['txt','csv']
blacklist_dir = get_full_path('data/blacklist.txt')


@app.route('/', methods=['GET', 'POST'])
def upload():
    blacklist = open(get_full_path(blacklist_dir)).read()
    if request.method == 'POST':
        file = request.files['file']
        session.clear()
        if file and allowed_file(file.filename):
            filename = get_file_name(file.filename)
            if black_checker(filename):
                return render_template('base.html', blacklist=open(blacklist_dir).read(), message='This sender has been blacklisted!!')
            else:
                content = file.read()
                detect = predict(content)
                if detect == 'fraud':
                    update_blacklist(filename)
                    return render_template('base.html',content=content,blacklist=open(blacklist_dir).read(),
                                           message=' This is a fraudulent mail.'
                                                   'Therefore,the mail has been updated on the blacklist')
                elif detect == 'ham':
                    render_template('base.html', blacklist=blacklist,content=content)
                elif detect == 'spam':
                    return render_template('base.html', blacklist=blacklist,
                                           message='This mail is spam, therefore it will be sent to spam folder')
                redirect(url_for('upload', blacklist=blacklist, content=content))
        return render_template('base.html', blacklist=blacklist, content=file.read())
    else:
        return render_template('base.html', blacklist=blacklist)


@app.errorhandler(400)
def page_not_found(e):
    return render_template('400.html')


def black_checker(filename):
    black_list = open(blacklist_dir).read()
    if filename in black_list:
        return True
    else:
        return False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_file_name(filename):
    return '.' in filename and filename.rsplit('.', 1)[0]


def update_blacklist(email):
    emails = open(blacklist_dir).read().split(',')
    emails.append(email)
    with open(blacklist_dir, 'w') as f:
        f.write(','.join(emails))
    f.close()


if __name__ == '__main__':
    nltk.data.path.append(get_full_path('nltk_data'))
    app.run(host='127.0.0.1', port=5000, debug=True)

from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename, redirect
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
df = pd.read_excel("Book.xlsx")


@app.route('/')
def hello_world():
    return render_template("index.html")


def read_list(file):
    global df
    df = pd.read_excel(file)
    print(df)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        read_list(f)
        return redirect(url_for('choose_column'))


@app.route('/choose', methods=['GET', 'POST'])
def choose_column():
    columns = df.columns
    print(columns)
    return render_template('choose.html', cols=columns)


@app.route('/uploadpage', methods=['GET', 'POST'])
def upload_page():
    return render_template("upload.html", df=df)


@app.route('/printlist', methods=['GET', 'POST'])
def print_list():
    if request.method == 'POST':
        contact_tag = request.form.get("contact_tag")
        name_tag = request.form.get('name_tag')
        cols = [contact_tag, name_tag]
    return render_template("listpage.html", contact_tag=contact_tag,name_tag=name_tag, df=df)


if __name__ == '__main__':
    app.run()

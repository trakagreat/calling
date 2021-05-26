from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename, redirect
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
df = None


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

        return render_template("list.html", df=df)


if __name__ == '__main__':
    app.run()

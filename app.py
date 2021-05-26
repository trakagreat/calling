from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename, redirect
import pandas as pd

app = Flask(__name__)

df = None

@app.route('/')
def hello_world():
    return render_template("index.html")

def read_list(file):
    global df
    df = pd.read_excel(file)
    print(df)
    return "uploade"


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        read_list(f)

        return render_template("list.html",df=df)







if __name__ == '__main__':
    app.run()

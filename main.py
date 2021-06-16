from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename, redirect
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
df = pd.read_excel("Book.xlsx")
col_index = None

@app.route('/')
def hello_world():
    return render_template("index.html")


def cleaning_df():
    df.dropna(axis=0, thresh=5, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)


def read_list(file):
    global df
    df = pd.read_excel(file)
    cleaning_df()


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        read_list(f)
        return redirect(url_for('choose_column_index'))


@app.route('/choose_col_index', methods=['GET', 'POST'])
def choose_column_index():
    columns = df.columns
    # head_rows = df.
    print(columns)
    return render_template('choose2.html', cols=columns, df=df)


@app.route('/choose_col', methods=['GET', 'POST'])
def choose_col():
    global df
    global col_index
    if request.method == "POST":
        col_str =request.form.get("column_index")
        print(col_str)
        if col_str == "default":
            cols = df.columns
        else:
            col_index = int(col_str)
            df.columns = df.iloc[col_index]
            # df.drop(index=col_index, inplace=True)

            cols = df.columns

        print(f"new columns  {cols}")
        print(f"col index: {col_index}")

    return render_template('choose.html', cols=cols, df=df, col_index=col_index)


@app.route('/uploadpage', methods=['GET', 'POST'])
def upload_page():
    return render_template("upload.html", df=df)


@app.route('/printlist', methods=['GET', 'POST'])
def print_list():
    if request.method == 'POST':
        contact_tag =df.columns[int(request.form.get("contact_tag"))]
        name_tag =df.columns[int(request.form.get('name_tag'))]
        cols = [contact_tag, name_tag]
        print(cols)

    return render_template("listpage.html", contact_tag=contact_tag, name_tag=name_tag, df=df,col_index=col_index)


if __name__ == '__main__':
    app.run()

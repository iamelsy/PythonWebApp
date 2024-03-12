import pandas as pd
import nltk
from flask import request
from flask import jsonify
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    #return "Hello World"
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    years = request.form['years']
    prev_sales = [('1', 300),
            ('2', 500),
            ('3', 600),
            ('4', 550),
            ('5', 530)]
    df = pd.DataFrame(prev_sales, columns=['Year', 'Sales'])

    X = df['Year']
    y = df['Sales']

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    from sklearn.linear_model import Lasso
    model = Lasso(alpha=100)
    model.fit(pd.DataFrame(X_train), pd.DataFrame(y_train))
    y_pred = model.predict(pd.DataFrame(X_test))
    lst=[]
    for i in range(6,6+int(years)):
        lst.append(int(model.predict(pd.DataFrame([i]))[0]))

    # Evaluate the model
    from sklearn.metrics import r2_score
    score = r2_score(y_test, y_pred)
    return redirect(url_for("newpage", sales=lst, accuracy=score))


@app.route('/new/<sales>')
def newpage(sales):
    return render_template('new_page.html', sales=sales)


if __name__ == "__main__":
    app.run(port='8088', threaded=False)

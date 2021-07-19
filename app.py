from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQL_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#Database Models

class User(db.Model):
    __tablename__ = "LexusF"
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(50))
    dealer = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self,customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods=['POST'])
def submit():
      if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        #print(customer, dealer, rating, comments) #Those values are printed in the terminal
       
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields ')
        
        if db.session.query(User).filter(User.customer == customer).count() == 0:
            data = User(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted')



if __name__ == '__main__':
    app.debug = True
    app.run()
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, InputRequired
import random

import os
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database1.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Mi clave super secreta"

db = SQLAlchemy(app)


preg = db.Table('preg',
    db.Column('test_id', db.Integer, db.ForeignKey('test.test_id')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.question_id'))
    )

class Test(db.Model):
    # Status = 0 -> DONE
    test_id = db.Column(db.Integer, primary_key = True)
    month = db.Column(db.String(50), nullable = False)
    preguntas  = db.relationship('Question', secondary =preg, backref=db.backref('preguntas', lazy='dynamic'))
    # created_on = db.Column(db.DateTime(), default=datetime.utcnow)

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key= True)
    question_text = db.Column(db.String(20))
    # question_option1 = db.Column(db.Integer, nullable = False)
    # question_option2 = db.Column(db.Integer, nullable = False)
    # question_option3 = db.Column(db.Integer, nullable = False)
    # question_option4 = db.Column(db.Integer, nullable = False)
    # question_ok = db.Column(db.Integer, nullable = False)
    # created_on = db.Column(db.DateTime(), default=datetime.utcnow)

@app.route("/create")
def add():
    db.create_all()
    return "GOL"

@app.route("/add1")
def add_task():
            # question_text = "Pregunta1"
            new_question1 = Question(question_text = "qqqqq")
            db.session.add(new_question1)
            question_text = "Pregunta2"
            new_question2 = Question(question_text = question_text)
            db.session.add(new_question2)
            test_text = "Examen1"
            new_test1 = Test(month = test_text)
            db.session.add(new_test1)
            test_text = "Examen2"
            new_test2 = Test(month = test_text)
            db.session.add(new_test2)
            new_question2.preguntas.append(new_test2)
            # db.session.commit()
            # new_question8.preguntas.append(new_test2)
            # db.session.commit()
            # new_question2.preguntas.append(new_test2)
            # db.session.commit()
            # new_question5.preguntas.append(new_test3)
            # db.session.commit()
            # new_question4.preguntas.append(new_test3)
            # db.session.commit()
            # new_question2.preguntas.append(new_test4)
            # db.session.commit()
            # new_question1.preguntas.append(new_test4)
            # db.session.commit()
            # new_question6.preguntas.append(new_test4)
            # db.session.commit()
            # new_question10.preguntas.append(new_test4)
            # db.session.commit()
            db.session.commit()
            # # Funciona, tira los examenes vinculados a la pregunta
            # # task = new_question6.preguntas
            # # print("GOLLLL")
            # # return render_template("list.html", task=task)
            # #Funciona para tirar todas las preguntas incluidas en un examen
            # task = Question.query.filter(Question.preguntas.any(month="Examen2")).all()
            # return render_template("list.html", task=task)
            return("HOLA")



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

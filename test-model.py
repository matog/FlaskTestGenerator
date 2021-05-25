from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
import os
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database_.db"

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

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key= True)
    question_text = db.Column(db.String(20))


@app.route("/")
def index():
    db.create_all()
    return "GOL"

@app.route("/create")
def add():
    db.create_all()
    return "GOL"

@app.route("/add")
def add_task():
            question_text = "Pregunta1"
            new_question1 = Question(question_text = question_text)
            db.session.add(new_question1)
            question_text = "Pregunta2"
            new_question2 = Question(question_text = question_text)
            db.session.add(new_question2)
            question_text = "Pregunta3"
            new_question3 = Question(question_text = question_text)
            db.session.add(new_question3)
            question_text = "Pregunta4"
            new_question4 = Question(question_text = question_text)
            db.session.add(new_question4)
            question_text = "Pregunta5"
            new_question5 = Question(question_text = question_text)
            db.session.add(new_question5)
            question_text = "Pregunta6"
            new_question6 = Question(question_text = question_text)
            db.session.add(new_question6)
            question_text = "Pregunta7"
            new_question7 = Question(question_text = question_text)
            db.session.add(new_question7)
            question_text = "Pregunta8"
            new_question8 = Question(question_text = question_text)
            db.session.add(new_question8)
            question_text = "Pregunta9"
            new_question9 = Question(question_text = question_text)
            db.session.add(new_question9)
            question_text = "Pregunta10"
            new_question10 = Question(question_text = question_text)
            db.session.add(new_question10)
            test_text = "Examen1"
            new_test1 = Test(month = test_text)
            db.session.add(new_test1)
            test_text = "Examen2"
            new_test2 = Test(month = test_text)
            db.session.add(new_test2)
            test_text = "Examen3"
            new_test3 = Test(month = test_text)
            db.session.add(new_test3)
            test_text = "Examen4"
            new_test4 = Test(month = test_text)
            db.session.add(new_test4)
            test_text = "Examen5"
            new_test5 = Test(month = test_text)
            db.session.add(new_test5)
            test_text6 = "Examen6"
            new_test6 = Test(month = test_text)
            db.session.add(new_test6)
            db.session.commit()
            new_question6.preguntas.append(new_test2)
            db.session.commit()
            new_question8.preguntas.append(new_test2)
            db.session.commit()
            new_question2.preguntas.append(new_test2)
            db.session.commit()
            new_question5.preguntas.append(new_test3)
            db.session.commit()
            new_question4.preguntas.append(new_test3)
            db.session.commit()
            new_question2.preguntas.append(new_test4)
            db.session.commit()
            new_question1.preguntas.append(new_test4)
            db.session.commit()
            new_question6.preguntas.append(new_test4)
            db.session.commit()
            new_question10.preguntas.append(new_test4)
            db.session.commit()
            # Funciona, tira los examenes vinculados a la pregunta
            # task = new_question6.preguntas
            # print("GOLLLL")
            # return render_template("list.html", task=task)
            #Funciona para tirar todas las preguntas incluidas en un examen
            task = Question.query.filter(Question.preguntas.any(test_id="16")).all()
            return render_template("list0.html", task=task)

@app.route("/1")
def test():
        return "HOLA"

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

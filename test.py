from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text

app = Flask(__name__)
app.secret_key = "secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + 'nilaygaitonde' + ":" + 'Nilay0309' + "@" + 'localhost:3306' + "/" + 'nodemysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(140))
    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/add',methods=['POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        post = Test(title,body)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('hello_world'))

@app.route('/delete/<id>')
def delete(id):
    post = Test.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('hello_world'))

@app.route('/display',methods=['GET'])
def display():
    post = Test.query.all()
    inspector = db.inspect(db.engine)
    return render_template('display.html',Test=post,columns=inspector.get_columns('Test'))
     
@app.route('/filter',methods=['GET'])
def like_filter():
    column_to_filter = request.args.get('filter')
    print(column_to_filter)
    like = request.args.get('like')
    stuff = f"Test.{column_to_filter}.like(%{like}%)"
    post = db.session.query(Test).filter(getattr(Test, column_to_filter).like(f'%{like}%')).all()
    inspector = db.inspect(db.engine)
    return render_template('display.html',Test=post,columns=inspector.get_columns('Test'))

if __name__ == '__main__':
    app.run(debug=True)
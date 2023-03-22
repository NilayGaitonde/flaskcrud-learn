from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text

app = Flask(__name__)
app.secret_key = "secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + 'nilaygaitonde' + ":" + 'Nilay0309' + "@" + 'localhost:3306' + "/" + 'customer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()
db = SQLAlchemy(app)

class Customers(db.Model):
    id = db.Column('id',db.Integer, primary_key=True)
    Name=db.Column(db.Text)
    Mobile=db.Column(db.Text)
    Email_Id=db.Column('Email Id',db.Text)
    Adress=db.Column(db.Text)
    City=db.Column(db.Text)
    State=db.Column(db.Text)
    Pincode=db.Column(db.Text)
    DOB=db.Column(db.DateTime)
    Pan_Id=db.Column('Pan Id',db.Text)
    Annual_Income=db.Column('Annual Income',db.Text)
    Payment_Bank=db.Column('Payment Bank',db.Text)
    Payment_Mode=db.Column('Payment Mode',db.Text)
    Type_of_Acc=db.Column('Type of Acc',db.Text)
    District=db.Column(db.Text)
    Locality=db.Column(db.Text)
    Sum_Insured=db.Column('Sum Insured',db.Text)
    Plan_Type=db.Column('Plan Type',db.Text)
    Proof_Id=db.Column('Proof Id',db.Text)
    Proff2=db.Column(db.Text)
    Locality1=db.Column('Locality.1',db.Text)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/add',methods=['POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        post = Customers(title,body)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('hello_world'))

@app.route('/delete/<id>')
def delete(id):
    post = Customers.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('hello_world'))

@app.route('/display',methods=['GET'])
def display():
    page = request.args.get('page', 1, type=int)
    post = Customers.query.limit(1000).all()
    inspector = db.inspect(db.engine)
    return render_template('display.html',Customers=post,columns=inspector.get_columns('Customers'),pagination=Customers.query.paginate(per_page=1000, page=page, error_out=True))
     
@app.route('/filter',methods=['GET','POST'])
def like_filter():
    if request.method == 'POST':
        page = request.args.get('page', 1, type=int)
        column_to_filter = request.args.get('filter')
        like = request.args.get('like')
        post = db.session.query(Customers).filter(getattr(Customers, column_to_filter).like(f'%{like}%')).all()
        inspector = db.inspect(db.engine)
    else:
        page = request.args.get('page', 1, type=int)
        post = Customers.query.limit(1000).all()
        inspector = db.inspect(db.engine)
    return render_template('display.html',Customers=post,columns=inspector.get_columns('Customers'),pagination=Customers.query.paginate(per_page=1000, page=page, error_out=True))

if __name__ == '__main__':
    app.run(debug=True)
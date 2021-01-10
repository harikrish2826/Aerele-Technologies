from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from datetime import datetime
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.sql.operators import from_
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from msilib import type_nullable



app = Flask(__name__)
engine = create_engine('sqlite:///C:\\sqlitedbs\\database.db')
app.config['SECRET_KEY']="flask"
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'product'                 
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    quantity=db.Column(db.Integer)
    def __init__(self,id,name,quantity):
        self.id=id
        self.name=name
        self.quantity=quantity      
        
    def __repr__(self):
        return '<Product %r>' %self.id

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(50))
    def __init__(self,id,name):
        self.id=id
        self.name=name
        
    def __repr__(self):
        return '<Location %r>' %self.id
    
class Movement(db.Model):
    __tablename__='productmovement'
    mid=db.Column(db.Integer,primary_key=True)
    from_location=db.Column(db.String(25))
    to_location=db.Column(db.String(25))
    pro_id=db.Column(db.String(25))
    quantity=db.Column(db.Integer)
    def __init__(self,f,t,p,q):
        self.from_location=f
        self.to_location=t
        self.pro_id=p
        self.quantity=q

    def __repr__(self):
        return '<Movement %r>' %self.id

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products',methods=["GET","POST"])
def products():
    
    if request.method=="GET":
        p = Product.query.all()
        return render_template('products.html',products=p)

    
    if request.method == "POST":
        pid=request.form["pid"]
        proname= request.form["pname"]
        pquantity=request.form["quantity"]
        new = Product(id=pid,name=proname,quantity=pquantity)
        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/products')
        except:
            return("Enter the valid Response")
        
    
@app.route('/locations',methods=["GET","POST"])
def locations():
    if request.method=="GET":
        l = Location.query.all()
        return render_template('locations.html',locations=l)

    if request.method == "POST":
        lid=request.form["lid"]
        lname = request.form["lname"]
        new = Location(id=lid,name=lname)
        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/locations')
        except:
            return("Enter the valid Response")



@app.route('/movements',methods=["GET","POST"])
def movements():
    if request.method=="GET":
        l=Location.query.all()
        p=Product.query.all()
        m=Movement.query.all()
        return render_template('m.html',locations=l,products=p,movements=m)
    
    if request.method=="POST":
        to=request.form["to-location"]
        from2=request.form["from-location"]
        p=request.form["product"]
        q=request.form["quantity"]
        
        if from2=='none':
            new=Movement(f=from2,t=to,p=p,q=q)
            try:
                db.session.add(new)
                db.session.commit()
                return redirect('/movements')
            except:
                return("Enter the valid Response")
        
@app.route('/report')
def report():
    locations = Location.query.all()
    products = Product.query.all()
    loc=[]
    pro=[]
    for l in locations:
        loc.append(l)
    for p in products:
        pro.append(p)
    n=len(loc)+len(pro)
    r=[]
    for i in range(n):
        r.append(loc[i])
        r.append(pro[i])
    return render_template('report.html',report=r)

@app.route("/products/updateproduct",methods=["GET","POST"])
def updateproduct():
    if request.method=="GET":
        return render_template("up.html")
    if request.method=="POST":
        proid=request.form["upid"]
        proname=request.form["quan"]
      
        return redirect('/products')
    
        
@app.route("/locations/updatelocation",methods=["GET","POST"])
def updatelocation():
    if request.method=="GET":
        return render_template("ul.html")
    if request.method=="POST":
        locid=request.form["upid"]
        locname=request.form["quan"]
        
        return redirect('/locations')

@app.route("/products/deleteproduct",methods=["GET","POST"])
def deleteproduct():
    if request.method=="GET":
        return render_template("deleteproduct.html")
    if request.method=="POST":
        proid=request.form["upid"]
        try:
            s=sessionmaker(bind=engine)
            s1=s()
            d=s.query(Product).get(proid)
            s.delete(d)
            return redirect('/products')
        except:
            return "Error"

@app.route("/locations/deletelocation",methods=["GET","POST"])
def deletelocation():
    if request.method=="GET":
        return render_template("deletelocation.html")
    if request.method=="POST":
        lid=request.form["upid"]
        try:
            s=sessionmaker(bind=engine)
            s1=s()
            d=s.query(Location).get(lid)
            s.delete(d)
            return redirect('/locations')
        except:
            return "Error"
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy is a popular SQL toolkit and Object Relational Mapper.
from datetime import datetime
# Flask constructor takes the name of   
# current module (__name__) as argument.
app=Flask(__name__)
 #The database URI that should be used for the connection.    #If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals. The default is None, which enables tracking but issues a warning that it will be disabled by default in the future. This requires extra memory and should be disabled if not needed.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" #used to create a database of that name given in the URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #compilr gives warning for signal emmiting purpose we are setting it to false
db = SQLAlchemy(app)#gives app data to db variable

#defining database schema using class  #The term "schema" refers to the organization of data as a blueprint of how the database is constructed
class Todo(db.Model):#here model is representing table
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str: #show you what u wanrt to see while priting
        return f"{self.sno} - {self.title}"



# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call which  associated function.
@app.route('/', methods=['GET','POST'])#here slash is a end point home page
def index():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
    #Inserting data into the database is a three step process:1)Create the Python object 2)Add it to the session 3)Commit the session
        todo=Todo(title=title,desc=desc)#creating a instance  
        db.session.add(todo)
        db.session.commit()
    
    allTodo=Todo.query.all()#to acess data from database in vs code 
    return render_template('test2.html',allTodo=allTodo)#to use python variable in jinja2  pass the variable in render template

@app.route("/about")
def about():
    return render_template("about.html")  

@app.route('/show')
def show():
    allTodo=Todo.query.all()#to acess data from database in vs code 
    print(allTodo)
    return "this is show page" 

@app.route('/update/<int:sno>' , methods=['GET', 'POST'])
def update(sno):# sno selected is passed and the respective record is chosen
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()#to acess data from database in vs code #  accordin to the serial number passsed the record is chosen#to acess data from database in vs code 
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")




if __name__ =="__main__":
    app.run(debug=True,port=8000)# run() method of Flask class runs the application on the local development server.

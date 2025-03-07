from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


with app.app_context():
    class Todo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.String(200), nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.utcnow)

        def __repr__(self):
            return '<Task %r>' % self.id

   
    db.create_all()

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST": 
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(desc("date_created")).all()
        return render_template('index.html', tasks=tasks)
@app.route('/delete/<int:id>',methods=['post',"get"])
def delete_task(id):
    deletable_task = Todo.query.get_or_404(id)
    try:
        db.session.delete(deletable_task)
        db.session.commit()
        return redirect('/')
    except:
        return "There was error deleting this task"
@app.route('/update/<int:id>',methods=["post","get"])
def update_task(id):
    task = Todo.query.get_or_404(id)
    if request.method=="POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating that task"
    else:
        return render_template("update_task.html",task=task)


if __name__ == "__main__":
    app.run(debug=True)

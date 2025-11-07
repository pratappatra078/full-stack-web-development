from flask import Flask,render_template,url_for,request,redirect
import random 
app = Flask(__name__)

todos =[
    {
        'id' : 1,
        'name' : 'Write SQL ',
        'checked': False,
    },
    {
        'id' : 1,
        'name' : 'Write Python ',
        'checked': True,
    },
]
@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
def home():
    if (request.method == "POST"):
        todo = request.form["todo_name"]
        curr_id = random.randint(1,1000)
        todos.append({
            'id': curr_id,
            'name':todo,
            'checked': False
        })
    return render_template("index.html",items=todos)

@app.route("/checked/<int:todo_id>",methods = ["POST"])
def checked_todo(todo_id):
    for todo in todos:
        if todo_id ==todo['id']:
            todo['checked'] = not todo['checked']
            break
    return redirect(url_for("home"))
@app.route('/delete/<int:todo_id>',methods=["POST"])
def delete_todo(todo_id):
    global todos
    for todo in todos:
        if todo_id == todo['id']:
            todos.remove(todo)

    return redirect(url_for("home"))

@app.route("/about")
def about():
    return render_template("about.html")
if __name__ =="__main__":
    app.run(debug=True)


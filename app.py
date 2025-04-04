from bson import ObjectId
from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:rootpassword@localhost:27017/scrum_flow?authSource=admin"
mongo = PyMongo(app)


@app.route('/')
def home():
    tasks = mongo.db.tasks.find()
    sprints = mongo.db.sprints.find()

    return render_template("index.html", tasks=tasks, sprints=sprints)


@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')

    if task_name:
        mongo.db.tasks.insert_one(
            {
                'name': task_name,
                'done': False
            }
        )

    return redirect('/')


@app.route('/add_sprint', methods=['POST'])
def add_sprint():
    sprint_name = request.form.get('sprint_name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if sprint_name and start_date and end_date:
        mongo.db.sprints.insert_one({
            'name': sprint_name,
            'start_date': start_date,
            'end_date': end_date
        })

    return redirect('/')


@app.route('/assign_task_to_sprint', methods=['POST'])
def assign_task_to_sprint():
    sprint_id = request.form.get('sprint_id')
    task_id = request.form.get('task_id')

    if sprint_id:
        mongo.db.tasks.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': {'sprint_id': ObjectId(sprint_id)}}
        )

    return redirect('/')


@app.route('/toggle_done/<task_id>', methods=['POST'])
def toggle_done(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    if task:
        new_done_status = not task['done']
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'done': new_done_status}})

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

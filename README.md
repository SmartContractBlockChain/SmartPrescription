# SmartPrescription

1. create virtual env. using conda

```
conda create --name smartPrescription python=3.9
```

2. activate virtual env.

```
conda activate smartPrescription
```

3. verify if you can begin the adventure by running hello_world.py

```
python hello_world.py
```

---

Using flask-restful to create a fast REST api app.

1. Install the dependencies

```
pip install requirements.txt
```

2. Run the flask server

```
python main.py
```

To test:
Get the full list : `curl http://localhost:5000/todos`
Get a single task : `curl http://localhost:5000/todos/todo3`
Delete a task : `curl http://localhost:5000/todos/todo2 -X DELETE -v`
Add a new task : `curl http://localhost:5000/todos -d "task=something new" -X POST -v`
Update a task : `curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v`

Reference: https://flask-restful.readthedocs.io/en/latest/index.html

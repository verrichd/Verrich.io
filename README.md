# ![img](docs/static/verrich_io_logo.png)

## __About Verrich.io__
Verrich.io is a data processing tool that can be used to develop and execute an ETL Pipeline using a Directed Acyclic Graph (DAG) for topological sorting based on task dependencies.

---
## __Project Structure__
This project structure should be used to help contributors understand where to "find" things and where to "put" new things. 

*   `.config` - This folder for configuration files including database.ini for connection parameters.
*   `docs` - Documentation about Verrich.io Workflows Package.
*   `examples` - Jupyter notebook file explaining Directed Acyclic Graphs
*   `src` - This is the source code folder containing all application code and modules.
*    `samples` - Currently holds workflow example using PostgreSQL dvdrental database. This is the place for adding any specific examples.
* `common` holds task and workflows scripts (i.e. the bread and butter of this program). Workflows are Pipelines that hold a queue filled with Tasks which are objects that perform a specified function.
* `data` contains pictures of generated DAG graphs as a result of using print function in DirectedAcyclicGraph class.
* `utils` holds executors, schedulers, graphs, and queues. A few design patterns including a Factory and Singleton will be found in these files.
*  `main` is the entry point of the program that is used to run sample workflows.
*  `LICENSE` - Open source license markdown
*  `README` - Markdown file describing the project
*   `requirements.txt` - list of python libraries to install with `pip` 

---

## __Getting Started__

### __Basic Usage__
The intended usage of this program to author a workflow that follows the ETL (Extract, Transform, and Load) design. A complete workflow pipeline should include 

1. `Setup()` will establish a database connection and create tables in a new schema (data warehouse)
2. `Extract()` will use the established connection to extract information from tables in the original schema into a Data Frame using the Pandas library.
3. `Transform()` will take the Data Frames created during `Extract`, and format them into a structure that matches the data warehouse schema.
4. `Load()` will take the formatted Data Frames from the `Transform` and load into the new schema using the same connection as created in `setup`.
5. `Teardown()` closes connection to the database.
---
### Code Examples
The following example shows how a user should create a Task which is the basic building block of an ETL Pipeline.
```python
from common.task import Task
from common.workflows import Pipeline

def createSchema(conn,name:str):
    """_summary_ This function creates a new schema for a database
    in an established connection using given name

    Args:
        conn (Connection): _description_ database connection
         must be established prior to calling this function
        name (str): _description_ is the name of the schema to be created
    """
    # Builds the SQL command to create schema
    query = "CREATE SCHEMA IF NOT EXISTS " + name + ';'
     
    # Connection executes constructed query 
    conn.execute(query) 

s = {}
s[1] = Task('schema',createSchema,{'connection':'conn'},
            kwargs={'conn':s[0].result,'name':'dw'})

# Create a pipeline with a list of Tasks
p = Pipeline(list(s.values()))
```

Continuing with the above example, multiple tasks should be constructed and stored in a list-like object for easy insertion into a DAG and/or Pipeline.
```python
from common.task import Task
from common.workflows import Pipeline
from utils.graph import DirectedAcyclicGraph

# 's' is a dictionary in this example but can be any data container that will easily produce a list of Task objects.
s = {}
s[0] = Task('connection',f.config_connect,[],{})
s[1] = Task('schema',f.createSchema,{'connection':'conn'},
            kwargs={'conn':s[0].result,'name':'dw'})
s[2] = Task('create_store',f.createTable,{'connection':'conn'},
            kwargs={'conn':s[0].result,'schema':'dw','query':q.create_store_table})
s[3] = Task('create_staff',f.createTable,{'connection':'conn'},
            kwargs={'conn':s[0].result,'schema':'dw','query':q.create_staff_table})
s[4] = Task('create_customer',f.createTable,{'connection':'conn'},
            kwargs={'conn':s[0].result,'schema':'dw','query':q.create_customer_table})
s[5] = Task('create_film',f.createTable,{'connection':'conn'},
            kwargs={'conn':s[0].result,'schema':'dw','query':q.create_film_table})
s[6] = Task('create_date',f.createTable,{'connection':'conn'},
            kwargs={'conn':s[0].result,'schema':'dw','query':q.create_date_table})
s[7] = Task('create_fact_rental',f.createTable,{'connection':'conn'},
            kwargs={'conn':s[0].result,'schema':'dw','query':q.create_fact_rental_table})

# Store values of s in a list so we have a list of Tasks
setup = list(s.values())

# At this point we can create a Pipeline that will hold these tasks in their current order
pipe = Pipeline(setup)
```
If we want to run these tasks in the most efficient manner based on dependecies, we must construct a DAG
```python
# Alternatively, we can add these Tasks as nodes in a DirectedAcyclicGraph
G = DAG()
G.addNodes(setup)

# Notice in order to construct the DAG properly, we must define some edge relationships between Task nodes based on dependecies
edges = [(s[0],s[1]),(s[1],s[2]),(s[1],s[3]),(s[1],s[4]),(s[1],s[5]),(s[1],s[6]),
            (s[1],s[7])]
# Now add this list of (Task,Task) tuples to the DAG as edges
G.addEdges(edges)

# View and/or save this DAG using print method -- argument is path to saved png file
G.print('src/data/testDag.png')

# After verifying the DAG is constructed as intended, topologically sort the nodes into a list that can be constructed into a Pipeline
sortedTasks = G.sortTasks()
pipe = Pipeline(sortedTasks)
```
Executing a pipeline:
```python

# From the utils.executor file
def execute(pipe:Pipeline):
    startTime = time.time()
    if(not pipe.status.__eq__('Setup')):
        pipe.setup()
    while(not pipe.queue.empty()):
        currentTask = pipe.queue.get()
        print("Running Task: " + currentTask.name)
        currentTask.manage_dependencies(pipe.results)
        currentTask.run()
        pipe.results[currentTask.name] = currentTask.result
    pipe.status = 'Executed'
    print("Pipeline Executed in " + (time.time() - startTime).__str__() + ' seconds')           

# Some constructed pipeline
pipe = Pipeline(someTaskList)
# Execute the pipeline in a main() or authored workflow function
execute(pipe)
```

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
The following example shows the intended creation of a Task which is the basic building block of an ETL Pipeline.
```python
from common.task import Task
from common.workflows import Pipeline

def createSchema(conn,name:str):
    """_summary_ This function creates a new schema for a database
    in an established connection using given name

    Args:
        conn (Connection): _description_ database connection must be established prior to calling this function
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


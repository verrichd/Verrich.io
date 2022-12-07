from utils.executor import execute
import samples.functions as f
import samples.queries as q
from common.task import Task
from utils.graph import DirectedAcyclicGraph as DAG
from common.workflows import Pipeline


def ETL(public_schema:str,warehouse:str):  
    """Calling this function will extract data from the public_schema, transform
    it into a star schema data warehouse format, and load it into the warehouse. This
    function will also generate a graph in the data folder called testDag."""
    
    # Dictionary of Tasks that are responsible for the setup of the data warehouse
    # as well as the connection to the database and the creation of a new schema   
    s = {}
    s[0] = Task('connection',f.config_connect,[],{})
    s[1] = Task('schema',f.createSchema,{'connection':'conn'},
                kwargs={'conn':s[0].result,'name':warehouse})
    s[2] = Task('create_store',f.createTable,{'connection':'conn'},
                kwargs={'conn':s[0].result,'schema':warehouse,'query':q.create_store_table})
    s[3] = Task('create_staff',f.createTable,{'connection':'conn'},
                kwargs={'conn':s[0].result,'schema':warehouse,'query':q.create_staff_table})
    s[4] = Task('create_customer',f.createTable,{'connection':'conn'},
                kwargs={'conn':s[0].result,'schema':warehouse,'query':q.create_customer_table})
    s[5] = Task('create_film',f.createTable,{'connection':'conn'},
                kwargs={'conn':s[0].result,'schema':warehouse,'query':q.create_film_table})
    s[6] = Task('create_date',f.createTable,{'connection':'conn'},
                kwargs={'conn':s[0].result,'schema':warehouse,'query':q.create_date_table})
    s[7] = Task('create_fact_rental',f.createTable,{'connection':'conn'},
                kwargs={'conn':s[0].result,'schema':warehouse,'query':q.create_fact_rental_table})

    # Dictionary of Tasks that are responsible for extracting all necessary tables from the public
    # schema that will be needed in some form in the data warehouse.
    e = {}
    e[0] = Task('ext_staff',f.extractData,{'connection':'conn'},
                {'conn':s[0].result,'schema':public_schema,'tableName':'staff',
                    'columns':' staff_id , concat(first_name ,\' \', last_name) AS name , email '})
    e[1] = Task('ext_customer',f.extractData,{'connection':'conn'},
                {'conn':s[0].result,'schema':public_schema,'tableName':'customer',
                    'columns':' customer_id, concat(first_name,\' \', last_name) AS name, email'})
    e[2] = Task('ext_store',f.extractData,{'connection':'conn'},
                {'conn':s[0].result,'schema':public_schema,'tableName':'store',
                    'columns':' store_id, manager_staff_id, address_id '})
    e[3] = Task('ext_address',f.extractData,{'connection':'conn'},
                {'conn':s[0].result,'schema':public_schema,'tableName':'address',
                    'columns':' address_id, address, district, city_id'})
    e[4] = Task('ext_city',f.extractData,{'connection':'conn'},
                {'conn':s[0].result,'schema':public_schema,'tableName':'city',
                    'columns':' city_id, city, country_id'})
    e[5] = Task('ext_country',f.extractData,{'connection':'conn'},
                {'conn':s[0].result,'schema':public_schema,'tableName':'country',
                    'columns':' country_id, country'})
    e[6] = Task('ext_film',f.extractData,{'connection':'conn'},
                {'conn':s[0].result,'schema':public_schema,'tableName':'film',
                    'columns':' film_id, rating, length, rental_duration, language_id, release_year, title '})
    e[7] = Task('ext_lang',f.extractData,{'connection':'conn'},
                {'conn':s[0].result,'schema':public_schema,'tableName':'language',
                    'columns':' language_id, name '})
    e[8] = Task('ext_rental',f.extractData,{'connection':'conn'},
                {'conn':s[0].result,'schema':public_schema,'tableName':'rental',
                    'columns':""" rental_id,rental_date,inventory_id,customer_id,staff_id, 
                                            extract(EPOCH from rental_date)::int AS int_date, 
                                            extract(year from rental_date)::int AS year,
                                            extract(month from rental_date)::int AS month, 
                                            extract(day from rental_date)::int AS day """})
    e[9] = Task('ext_inventory',f.extractData,{'connection':'conn'}
                ,{'conn':s[0].result,'schema':public_schema,'tableName':'inventory',
                    'columns':' inventory_id, film_id, store_id '})

    # Dictionary of Tasks that transform the extracted data frames into new or formatted 
    # ones that are compatible with the data warehouse schema
    t = {}
    t[0] = Task('tran_date',f.formatDate,{'ext_rental':'data'},
                kwargs = {'data':e[8].result})
    t[1] = Task('tran_film',f.formatFilm,{'ext_film':'filmDF','ext_lang':'languageDF'},
                kwargs = {'filmDF':e[6].result,'languageDF':e[7].result})
    t[2] = Task('tran_store',f.formatStore,
                {'ext_store':'store','ext_staff':'staff','ext_address':'address',
                 'ext_city':'city','ext_country':'country'},
                kwargs = {'store':e[2].result,'staff':e[0].result,
                        'address':e[3].result,'city':e[4].result,'country':e[5].result})
    t[3] = Task('tran_staff',f.formatStaff,{'ext_staff':'staff'},
                kwargs = {'staff':e[0].result})
    t[4] = Task('tran_customer',f.formatCustomer,{'ext_customer':'customer'},
                kwargs = {'customer':e[1].result})
    t[5] = Task('tran_fact_rental',f.formatFactRental,{'ext_rental':'rental','ext_inventory':'inventory'},
                kwargs = {'rental':e[8].result,'inventory':e[9].result})


    # Dictionary with Tasks that load our transformed data frames into the data warehouse schema
    l = {}
    l[3] = Task('load_staff',f.loadData,{'tran_staff':'data','connection':'conn'},
                kwargs= {'conn':s[0].result,'data':t[3].result, 
                        'schema':warehouse, 'tblName':'staff'})
    l[1] = Task('load_film',f.loadData,{'tran_film':'data','connection':'conn'},
                kwargs= {'conn':s[0].result,'data':t[1].result, 
                        'schema':warehouse, 'tblName':'film'})
    l[2] = Task('load_store',f.loadData,{'tran_store':'data','connection':'conn'},
                kwargs= {'conn':s[0].result,'data':t[2].result, 
                        'schema':warehouse, 'tblName':'store'})
    l[0] = Task('load_date',f.loadData,{'tran_date':'data','connection':'conn'},
                kwargs= {'conn':s[0].result,'data':t[0].result, 
                        'schema':warehouse, 'tblName':'date'})
    l[4] = Task('load_customer',f.loadData,{'tran_customer':'data','connection':'conn'},
                kwargs= {'conn':s[0].result,'data':t[4].result, 
                        'schema':warehouse, 'tblName':'customer'})
    l[5] = Task('load_fact_rental',f.loadData,{'tran_fact_rental':'data','connection':'conn'},
                kwargs= {'conn':s[0].result,'data':t[5].result,
                        'schema':warehouse, 'tblName':'fact_rental'})
    
    # Generate lists of Tasks from each dictionary
    setup = list(s.values())
    extract = list(e.values())
    transform = list(t.values())
    load = list(l.values())
    
    # List of (Task, Task) tuples that represent directional dependency (edges in a DAG)
    edges =[(s[0],s[1]),(s[1],s[2]),(s[1],s[3]),(s[1],s[4]),(s[1],s[5]),(s[1],s[6]),
            (s[1],s[7]),(s[0],e[1]),(s[0],e[2]),(s[0],e[3]),(s[0],e[4]),(s[0],e[5]),
            (s[0],e[6]),(s[0],e[7]),(s[0],e[8]),(s[0],e[9]),(e[8],t[0]),(e[6],t[1]),
            (e[7],t[1]),(e[0],t[2]),(e[2],t[2]),(e[3],t[2]),(e[4],t[2]),(e[5],t[2]),
            (e[0],t[3]),(e[1],t[4]),(e[8],t[5]),(e[9],t[5]),(t[0],l[0]),(t[1],l[1]),
            (t[2],l[2]),(t[3],l[3]),(t[4],l[4]),(t[5],l[5])]
    
    # Construct and print the DAG
    G = DAG()
    G.addNodes(setup)
    G.addNodes(extract)
    G.addNodes(transform)
    G.addNodes(load)
    G.addEdges(edges)
    G.print({0:3,1:7,2:8,3:7,4:5},'src/data/testDag.png')
    
    # Topologically sort the Tasks based on dependencies
    sortedTasks = G.sortTasks()
    # Add a teardown Task to the end of the list
    sortedTasks.append(Task('teardown',f.teardown,{'connection':'conn'},{'conn':s[0]}))
    
    # Create a Pipeline using the sorted list of Tasks
    process = Pipeline(sortedTasks)
    # Execute the Pipeline
    execute(process)

 
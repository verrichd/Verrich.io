from configparser import ConfigParser
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def config_connect(path:str = '.config\database.ini', section:str = 'postgresql'):
    """_summary_ This function establishes a connection to a database given 
    credentials in a remote path in the project (typically config/database.ini)

    Args:
        path (str): _description_ path to the file containing database credentials
        section (str): _description_ section in the file that contains credentials

    Returns:
        Connection: _description_ connection to database
    """
     # Dictionary that will eventually hold database credentials
    credentials = {}
    
    # ConfigParser object that will read database.ini file
    parser = ConfigParser() 
    # Finding database.ini file using path parameter
    parser.read(path)  
    
    # Checking for specified section in file
    if parser.has_section(section): 
        # Assign items in section to params variable (list of tuples)
        params = parser.items(section)
        for k,v in params: 
            # Parses each tuple in the list params to populate credentials dictionary
            credentials[k] = v  
    
    # Creates connection using connection string and SQLAlchemy engine
    conn_string = f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['dbname']}"
    engine = create_engine(conn_string)
    conn = engine.connect()
    return conn
    

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
    
def createTable(conn,schema:str,query:str):
    """_summary_ Creates table in database schema (provided schema name exists)

    Args:
        conn (Connection): _description_ database connection
        schema (str): _description_ schema where table will be created
        query (str): _description_ contains table credentials in SQL query
    """
    # Frame provided query statement with CREATE TABLE command
    query = 'CREATE TABLE IF NOT EXISTS ' + schema + '.' + query
    query = query.replace('(schema)', schema, -1)
    
    # Connection executes constructed query to create table
    conn.execute(query)
   
    
def extractData(conn,schema:str,tableName:str, columns:list[str]|str) -> pd.DataFrame:
    """_summary_ This function collects information in specified columns
    from a table in the given schema

    Args:
        conn (Connection): _description_ database connection
        schema (str): _description_ schema that contains the table
        tableName (str): _description_ name of the table containing the data
        columns (list[str] | str): _description_ list of column names in the 
        table that will be extracted

    Returns:
        pd.DataFrame: _description_ A dataframe containing the data that results from the 
        query to the columns in the table specified in the arguments
    """
    df = pd.read_sql("SELECT " + columns + " FROM " + schema + '.' + tableName , conn)
    return df

def loadData(conn, data:pd.DataFrame,schema:str,tblName:str):
    """_summary_ This function will load data from a data frame into a schema inside a 
    database provided a connection, schema, and table name

    Args:
        conn (Connection): _description_ database connection
        data (pd.DataFrame): _description_ dataframe containing data to be loaded
        schema (str): _description_ name of the schema containing the table
        tblName (str): _description_ name of the table to be loaded with data
    """
    data.to_sql(tblName,conn,schema = schema,if_exists='append',index=False)


def formatDate(data:pd.DataFrame) -> pd.DataFrame:
    """_summary_ Formats the rental table extracted from database
    into a format that is compatible with the newly designed schema.
    Transformations include adding a column for quarter that is derived 
    from the month column.

    Args:
        data (pd.DataFrame): _description_ dataframe of rental table in database

    Returns:
        pd.DataFrame: _description_ dataframe(sk_date,year,month,day,quarter)
    """
    newDF = dict()
    newDF['sk_rental'] = data['rental_id']
    newDF['date'] = data['int_date']
    newDF['year'] = list(data['year'])
    newDF['month'] = list(data['month'])
    newDF['day'] = list(data['day'])
    newDF['quarter'] = np.asarray(newDF['month'])
    newDF['quarter'] = newDF['quarter']//4 + 1
    
    return pd.DataFrame(newDF)

def formatFilm(filmDF:pd.DataFrame,languageDF:pd.DataFrame) -> pd.DataFrame:
    """_summary_ Formats the film dataframe created during extraction from the film
    table in the public schema. Transformations include mapping language_id to name of
    the language using a dictionary created with the language dataframe.

    Args:
        filmDF (pd.DataFrame): _description_ original film dataframe from extraction
        languageDF (pd.DataFrame): _description_ language datafram from extraction

    Returns:
        pd.DataFrame: _description_ new dataframe with language name in place of language_id
    """
    newDF = filmDF.copy()
    language_dict = dict(zip(languageDF['language_id'],languageDF['name']))
    filmDF['language'] = filmDF['language_id'].map(language_dict)
    newDF = newDF.drop('language_id',axis=1)
    newDF = newDF.rename(columns = {'film_id':'sk_film',
                         'rating':'rating_code',
                         'length':'film_duration'})
    return newDF

def formatStore(store:pd.DataFrame,staff:pd.DataFrame,
                address:pd.DataFrame,city:pd.DataFrame,
                country:pd.DataFrame)->pd.DataFrame:
    """_summary_ Formats the store dataframe created during extraction. Utilizes same strategy
    as seen in formatFilm function: create dictionary using other dataframe parameters, then use
    dictionary to add column to store dataframe. Then delete excess columns containing foreign key id's

    Args:
        store (pd.DataFrame): _description_ original store dataframe from extraction
        staff (pd.DataFrame): _description_ original staff dataframe from extraction
        address (pd.DataFrame): _description_ original address dataframe
        city (pd.DataFrame): _description_ original city dataframe
        country (pd.DataFrame): _description_ original country dataframe

    Returns:
        pd.DataFrame: _description_ new dataframe(sk_store,name,address,city,state,country)
    """
    newDF = pd.DataFrame(store)
    staff_dict = dict(zip(staff['staff_id'], staff['name']))
    address_dict = dict(zip(address['address_id'], address['address']))
    city_dict = dict(zip(city['city_id'],city['city']))
    address['city'] = address['city_id'].map(city_dict)
    address_to_city_dict = dict(zip(address['address_id'], address['city']))
    country_dict = dict(zip(country['country_id'],country['country']))
    city['country'] = city['country_id'].map(country_dict)
    city_to_country_dict = dict(zip(city['city_id'],city['country']))
    address['country'] = address['city_id'].map(city_to_country_dict)
    address_to_country_dict = dict(zip(address['address_id'],address['country']))
    state_dict = dict(zip(address['address_id'],address['district']))
    newDF['sk_store'] = store['store_id']
    newDF['name'] = store['manager_staff_id'].map(staff_dict)
    newDF['address'] = store['address_id'].map(address_dict)
    newDF['city'] = store['address_id'].map(address_to_city_dict)
    newDF['state'] = store['address_id'].map(state_dict)
    newDF['country'] = store['address_id'].map(address_to_country_dict)
    newDF = newDF.drop(['store_id' ,'manager_staff_id','address_id'],axis = 1)
    return newDF
    
    
def formatStaff(staff:pd.DataFrame) -> pd.DataFrame:
    """_summary_ Formats staff table into compatible structure for planned star schema

    Args:
        staff (pd.DataFrame): _description_ original dataframe extracted from database staff table

    Returns:
        pd.DataFrame: _description_ dataframe with changes made to column names
    """
    newDF = pd.DataFrame(staff)
    newDF = newDF.rename(columns={'staff_id':'sk_staff'})
    return newDF
    
def formatCustomer(customer:pd.DataFrame) -> pd.DataFrame:
    """_summary_ Formats customer table into compatible structure for planned star schema

    Args:
        staff (pd.DataFrame): _description_ original dataframe extracted from database customer table

    Returns:
        pd.DataFrame: _description_ dataframe with changes made to column names
    """
    newDF = pd.DataFrame(customer)
    newDF = newDF.rename(columns={'customer_id':'sk_customer'})
    return newDF
    
def formatFactRental(rental:pd.DataFrame,inventory:pd.DataFrame) -> pd.DataFrame:
    """_summary_ Formats fact_rental table using rental dataframe as a template. Some column names
    are changed to match new schema, and more columns are added using the dictionary mapping method
    as seen in the functions that format the store and film dataframes.

    Args:
        rental (pd.DataFrame): _description_ rental table extraction
        customer (pd.DataFrame): _description_ customer table extraction
        store (pd.DataFrame): _description_ store table extraction
        film (pd.DataFrame): _description_ film table extraction
        staff (pd.DataFrame): _description_ staff table extraction
        inventory (pd.DataFrame): _description_ inventory table extraction

    Returns:
        pd.DataFrame: _description_ new dataframe(sk_customer,sk_rental,
        sk_store,sk_film,sk_staff,count_rentals)
    """
    newDF = pd.DataFrame(rental)
    newDF = newDF.rename(columns={'customer_id':'sk_customer','staff_id':'sk_staff','rental_id':'sk_rental'})
    inv_to_store_dict = dict(zip(inventory['inventory_id'],inventory['store_id']))
    inv_to_film_dict = dict(zip(inventory['inventory_id'],inventory['film_id']))
    newDF['sk_store'] = newDF['inventory_id'].map(inv_to_store_dict)
    newDF['sk_film'] = newDF['inventory_id'].map(inv_to_film_dict)
    newDF = newDF.groupby(['sk_customer', 'sk_rental', 'sk_store', 'sk_film', 'sk_staff']).agg(count_rentals=('sk_film','count')).reset_index()
    
    return newDF
    
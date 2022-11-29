"""_summary_ = 'Contains functions that setup, extract, transform,
load, and teardown in the main file of the application
"""
import utils.functions as f
import data.queries as q
import pandas as pd

# Connection to the database (accessed globally)
conn = f.config_connect('.config\database.ini','postgresql')

# Data is a dictionary that will hold string keys representing extracted data frame values
data = dict()
transformed_data = dict()
def setup():
    """This function will  initialize tables, fields,
    and relationships in the data warehouse schema""" 
    
    f.createSchema(conn,'TEST')
    f.createTable(conn,'TEST',q.create_store_table)
    f.createTable(conn,'TEST',q.create_staff_table)
    f.createTable(conn,'TEST',q.create_customer_table)
    f.createTable(conn,'TEST',q.create_film_table)
    f.createTable(conn,'TEST',q.create_date_table)
    f.createTable(conn,'TEST',q.create_fact_rental_table)
    
    
def extract():
    """This function will extract the necessary data
    from the database connection and place into dataframes
    using the pandas library for future transformations"""

    data['staff_df'] = f.extractData(conn,'public','staff',' staff_id , concat(first_name ,\' \', last_name) AS name , email ')
    data['customer_df'] = f.extractData(conn, 'public', 'customer',' customer_id, concat(first_name,\' \', last_name) AS name, email')
    data['store_df'] = f.extractData(conn, 'public','store', ' store_id, manager_staff_id, address_id ')
    data['address_df'] = f.extractData(conn, 'public','address',' address_id, address, district, city_id')
    data['city_df'] = f.extractData(conn, 'public', 'city', ' city_id, city, country_id')
    data['country_df'] = f.extractData(conn, 'public','country',' country_id, country')
    data['film_df'] = f.extractData(conn, 'public','film', ' film_id, rating, length, rental_duration, language_id, release_year, title ')
    data['lang_df'] = f.extractData(conn, 'public','language',' language_id, name ')
    data['rental_df'] = f.extractData(conn, 'public', 'rental', """ rental_date,inventory_id,customer_id,staff_id, 
                                            extract(EPOCH from rental_date)::int AS int_date, 
                                            extract(year from rental_date)::int AS year,
                                            extract(month from rental_date)::int AS month, 
                                            extract(day from rental_date)::int AS day """)
    data['inventory'] = f.extractData(conn, 'public', 'inventory', ' inventory_id, film_id, store_id ')
    
    # for x in data:
    #     print(x)
    #     print(data[x])
    #     print()
    
    
    
def transform():
    """This function will perform a series of transformations on
    the extracted data already placed in dataframes"""
    dateDF = f.formatDate(data['rental_df'])
    print(dateDF)
    filmDF = f.formatFilm(data['film_df'],data['lang_df'])
    storeDF = f.formatStore(data['store_df'],data['staff_df'],
                            data['address_df'],data['city_df'],
                            data['country_df'])
    staffDF = f.formatStaff(data['staff_df'])
    customerDF = f.formatCustomer(data['customer_df'])
    fact_rentalDF = f.formatFactRental(data['rental_df'],data['customer_df'],
                                       data['store_df'],data['film_df'],
                                       data['staff_df'],data['inventory'])
    

def load():
    """This function will load all transformed data into the
    data warehouse star schema created during setup"""
    
def teardown():
    """This function will close any connections to the database"""
    conn.close()
    
    
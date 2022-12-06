"""This file contains SQL queries for creating tables in the data warehouse star schema"""


create_staff_table = """
staff
    (
        sk_staff integer NOT NULL,
        name character varying,
        email character varying,
        CONSTRAINT STAFF_pkey PRIMARY KEY (sk_staff)
    );
    """
    
create_customer_table = """
customer
    (
        sk_customer integer NOT NULL,
        name character varying,
        email character varying,
        CONSTRAINT CUSTOMER_pkey PRIMARY KEY (sk_customer)
    );
    """

create_date_table = """
date
    (
        sk_RENTAL integer NOT NULL UNIQUE,
        date integer NOT NULL,
        quarter integer,
        year integer,
        month integer,
        day integer,
        CONSTRAINT DATE_pkey PRIMARY KEY (sk_RENTAL)
    );    
    """
create_store_table = """
store
    (
        sk_store integer NOT NULL,
        name character varying,
        address character varying,
        city character varying,
        state character varying,
        country character varying,
        CONSTRAINT STORE_pkey PRIMARY KEY (sk_store)
    );
    """

create_film_table = """
film
    (
        sk_film integer NOT NULL,
        rating_code mpaa_rating,
        film_duration smallint,
        rental_duration smallint,
        language character(20),
        release_year year,
        title character varying(255),
        CONSTRAINT FILM_pkey PRIMARY KEY (sk_film)
    );
    """

create_fact_rental_table = """
fact_rental
    (
        sk_CUSTOMER integer,
        sk_RENTAL integer,
        sk_STORE integer,
        sk_FILM integer,
        sk_STAFF integer,
        count_rentals integer,
        CONSTRAINT sk_CUSTOMER FOREIGN KEY (sk_CUSTOMER) REFERENCES (schema).customer (sk_customer),
        CONSTRAINT sk_DATE FOREIGN KEY (sk_RENTAL) REFERENCES (schema).date (sk_RENTAL), 
        CONSTRAINT sk_FILM FOREIGN KEY (sk_FILM) REFERENCES (schema).film (sk_film) ,
        CONSTRAINT sk_STAFF FOREIGN KEY (sk_STAFF) REFERENCES (schema).staff (sk_staff) ,
        CONSTRAINT sk_STORE FOREIGN KEY (sk_STORE) REFERENCES (schema).store (sk_store)
    );
    """

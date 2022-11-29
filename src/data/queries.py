"""This file contains SQL queries for creating tables in the data warehouse star schema"""


create_staff_table = """
"STAFF"
    (
        sk_staff integer NOT NULL,
        name character varying COLLATE pg_catalog."default",
        email character varying COLLATE pg_catalog."default",
        CONSTRAINT "STAFF_pkey" PRIMARY KEY (sk_staff)
    );
    """
    
create_customer_table = """
"CUSTOMER"
    (
        sk_customer integer NOT NULL,
        name character varying COLLATE pg_catalog."default",
        email character varying COLLATE pg_catalog."default",
        CONSTRAINT "CUSTOMER_pkey" PRIMARY KEY (sk_customer)
    );
    """

create_date_table = """
"DATE"
    (
        sk_date integer NOT NULL,
        quarter character varying COLLATE pg_catalog."default",
        year integer,
        month integer,
        day integer,
        CONSTRAINT "DATE_pkey" PRIMARY KEY (sk_date)
    );    
    """
create_store_table = """
"STORE"
    (
        sk_store integer NOT NULL,
        name character varying COLLATE pg_catalog."default",
        address character varying COLLATE pg_catalog."default",
        city character varying COLLATE pg_catalog."default",
        state character varying COLLATE pg_catalog."default",
        country character varying COLLATE pg_catalog."default",
        CONSTRAINT "STORE_pkey" PRIMARY KEY (sk_store)
    );
    """

create_film_table = """
"FILM"
    (
        sk_film integer NOT NULL,
        rating_code mpaa_rating,
        film_duration smallint,
        language character(20) COLLATE pg_catalog."default",
        release_year year,
        title character varying(255) COLLATE pg_catalog."default",
        CONSTRAINT "FILM_pkey" PRIMARY KEY (sk_film)
    );
    """

create_fact_rental_table = """
"FACT_RENTAL"
    (
        "sk_CUSTOMER" integer,
        "sk_DATE" integer,
        "sk_STORE" integer,
        "sk_FILM" integer,
        "sk_STAFF" integer,
        count_rentals integer,
        CONSTRAINT "sk_CUSTOMER" FOREIGN KEY ("sk_CUSTOMER") REFERENCES (schema)."CUSTOMER" (sk_customer),
        CONSTRAINT "sk_DATE" FOREIGN KEY ("sk_DATE") REFERENCES (schema)."DATE" (sk_date), 
        CONSTRAINT "sk_FILM" FOREIGN KEY ("sk_FILM") REFERENCES (schema)."FILM" (sk_film) ,
        CONSTRAINT "sk_STAFF" FOREIGN KEY ("sk_STAFF") REFERENCES (schema)."STAFF" (sk_staff) ,
        CONSTRAINT "sk_STORE" FOREIGN KEY ("sk_STORE") REFERENCES (schema)."STORE" (sk_store)
    );
    """

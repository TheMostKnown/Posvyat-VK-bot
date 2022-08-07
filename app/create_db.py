import psycopg2
from vk_config import db_name, user_name, pswrd, port, host

def create():
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=user_name,
            password=pswrd,
            host=host,
            port=port
        )

        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE groups(
                id serial PRIMARY KEY,
                group_info varchar(15) NOT NULL
                );
                """
                """CREATE TABLE guests(
                id serial PRIMARY KEY,
                surname varchar(20) NOT NULL,
                name varchar(20) NOT NULL,
                patronymic varchar(20) NOT NULL,
                phone_number varchar(12) NOT NULL,
                tag varchar NOT NULL,
                vk_link varchar UNIQUE,
                first_group boolean NOT NULL,
                second_group boolean NOT NULL,
                third_group boolean NOT NULL,
                fourth_group boolean NOT NULL,
                fifth_group boolean NOT NULL,
                sixth_group boolean NOT NULL,
                seventh_group boolean NOT NULL,
                eighth_group boolean NOT NULL,
                ninth_group boolean NOT NULL,
                tenth_group boolean NOT NULL,
                eleventh_grup boolean NOT NULL,
                twelfth_group boolean NOT NULL,
                thirteenth_group boolean NOT NULL
                );
                """
                """CREATE TABLE orgs(
                id serial PRIMARY KEY, 
                surname varchar(20) NOT NULL,
                name varchar(20) NOT NULL,
                patronymic varchar(20) NOT NULL,
                vk_org_link varchar NOT NULL,
                first_org_group boolean NOT NULL,
                second_org_group boolean NOT NULL
                );
                """
                """CREATE TABLE sendings(
                mail_name varchar(20) PRIMARY KEY,
                send_time time NOT NULL,
                group_num int references groups,
                info varchar(500) NOT NULL,
                media varchar(50)
                );
                """
                """CREATE TABLE info(
                question varchar(100) PRIMARY KEY, 
                answer varchar(500) NOT NULL
                );
                """
                """CREATE TABLE tech_support(
                id serial PRIMARY KEY,
                vk_link varchar references guests(vk_link),
                per_question varchar(100) NOT NULL,
                status boolean NOT NULL
                );
                """
            )
            print("[INFO] Table created successfully")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def check_existance():

    try:
        connection = psycopg2.connect(
            database=db_name,
            user=user_name,
            password=pswrd,
            host=host,
            port=port
        )
        cursor = connection.cursor()
        cursor.execute("""SELECT name FROM guests;""")

    except Exception:
        create()

    else:
        print('[INFO] DB already exists!')


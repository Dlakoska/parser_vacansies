import os
from configparser import ConfigParser
import psycopg2
from config import ROOT_DIR


path = os.path.join(ROOT_DIR, 'database.ini')


def connect(filename="database.ini"):
    """
    Коннектор для соединения с БД. При вызове можно передать другие аргументы
    """
    config = ConfigParser()
    config.read(filename)
    database_date = dict(config.items('database'))
    conn = psycopg2.connect(host=database_date['host'],
                            port=database_date['port'],
                            database=database_date['database'],
                            user=database_date['user'],
                            password=database_date['password'])

    return conn


def create_tables(conn) -> None:
    """
    Создание таблиц в базе данных
    """
    with conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE employers (employer_id INT PRIMARY KEY, 
                                                   employer_name VARCHAR(100) NOT NULL)""")

            cur.execute("""CREATE TABLE vacancies (vacancy_id SERIAL PRIMARY KEY, 
                                                   employer_id INT REFERENCES employers(employer_id),
                                                   vacancy_name VARCHAR(100) NOT NULL,
                                                   salary INT NOT NULL,
                                                   currency VARCHAR(100),
                                                   requirement TEXT,
                                                   vacancy_url VARCHAR(100) NOT NULL)""")


def loads_into_table(conn, vacancies: list) -> None:
    """
    Заполняет таблицу данными о вакансиях
    """

    with conn:
        with conn.cursor() as cur:
            for vac in vacancies:
                cur.execute('INSERT INTO employers (employer_id, employer_name) VALUES '
                            '(%s,%s)' 'ON CONFLICT (employer_id) DO NOTHING', (vac.employer_id, vac.employer_name))

                cur.execute(
                    'INSERT INTO vacancies (employer_id, vacancy_name, salary, currency, '
                    'requirement, vacancy_url) VALUES '
                    '(%s,%s,%s,%s,%s, %s)',
                    (vac.employer_id, vac.vacancy_name, vac.salary, vac.currency,
                     vac.requirement, vac.vacancy_url))


def drop_table(conn, table_name) -> None:
    """
    Удаляет таблицу из базы данных
    """

    with conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE ")
            print(f'Из базы данных удалена таблица {table_name}')




class DBManager:
    """
    Класс для организации подключения и вывода информации из БД по определенным критериям
    """

    def __init__(self, conn):
        self.conn = conn

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute('SELECT  employers.employer_name, COUNT(*) FROM vacancies '
                            'JOIN employers USING(employer_id)'
                            'GROUP BY employers.employer_name')
                rows = cur.fetchall()
                for row in rows:
                    print(f"компания - {(row[0])}, количество вакансий - {row[1]}")

    def get_all_vacancies(self):
        """
        Получает список всех компаний с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute('SELECT * FROM vacancies')
                rows = cur.fetchall()
                for row in rows:
                    print(f'{row} \n {"-" * 200}')

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям в рублях
        """
        currency = "RUR"
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT AVG(salary) "
                            f"FROM vacancies "
                            f"WHERE vacancies.currency = %s", (currency,))
                rows = cur.fetchall()
                decimal_value = rows[0][0]
                if decimal_value is not None:
                    print(f"средняя зарплата - {int(decimal_value)} {currency}")

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий у которых зарплата выше средней по всем вакансиям
        """
        currency = "RUR"
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancies WHERE currency = %s "
                            f"AND salary > (SELECT AVG(salary) "
                            f"FROM vacancies "
                            f"WHERE currency = %s)", (currency, currency))
                rows = cur.fetchall()
                for row in rows:
                    print(f'{row} \n {"-" * 200}')

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        with self.conn:
            with self.conn.cursor() as cur:
                like_pattern = f"%{keyword.lower()}%"
                cur.execute(f"SELECT * FROM vacancies WHERE LOWER(vacancy_name)"
                            f" LIKE %s", (like_pattern,))
                rows = cur.fetchall()
                for row in rows:
                    print(f'{row} \n {"-" * 200}')

    def conn_close(self):
        """
        Закрывает соединение с БД
        """
        if self.conn:
            self.conn.close()

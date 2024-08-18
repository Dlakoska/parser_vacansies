import time
from src.api import HH
from src.dbmanager import DBManager
from src.utils import connect, create_tables, loads_into_table, drop_table


def main():
    """
    Пользовательский интерфейс приложения
    """

    conn = connect('database.ini')
    drop_table(conn, 'vacancies')
    drop_table(conn, 'employers')

    hh_api = HH()
    page_quantity = input('Введите количество запрашиваемых страниц от 1 до 20: ')

    # Проверка на кол-во введеных страниц, не больше 20, иначе выведем 2 по умолчанию
    if page_quantity.isdigit() and 0 < int(page_quantity) <= 20:
        hh_api.load_vacancies(int(page_quantity))
    else:
        print(f'вы ввели неверный параметр, по умолчанию будет загружено 20 страниц')
        time.sleep(1)
        hh_api.load_vacancies()

    vacancies_list = hh_api.vacancies
    vacancies_inst_list = hh_api.parse_vacancies(vacancies_list)
    create_tables(conn)
    loads_into_table(conn, vacancies_inst_list)
    db_man_inst = DBManager(conn)

    while True:
        print(f"1 - вывести на экран список всех компаний и количество вакансий у каждой компании\n"
              f"2 - вывести на экран список всех вакансий с указанием названия компании, названия вакансии и "
              f"зарплаты и ссылки на вакансию\n"
              f"3 - вывести на экран среднюю зарплату по вакансиям. (по умолчанию RUR)\n"
              f"4 - вывести на экран список всех вакансий, у которых зарплата выше средней по всем вакансиям. "
              f"(по умолчанию RUR)\n"
              f"5 - вывести на экран список всех вакансий, в названии которых содержится ключевое слово.\n"
              f"0 - завершение программы")

        choice_number = ['1', '2', '3', '4', '5', '0']
        user_choice = input(f"{'*' * 50}\nВведите номер и нажмите 'enter' для пуска действия: ")

        if user_choice and user_choice == '1' and user_choice in choice_number:
            db_man_inst.get_companies_and_vacancies_count()

        elif user_choice and user_choice == '2' and user_choice in choice_number:
            db_man_inst.get_all_vacancies()

        elif user_choice and user_choice == '3' and user_choice in choice_number:
            db_man_inst.get_avg_salary()

        elif user_choice and user_choice == '4' and user_choice in choice_number:
            db_man_inst.get_vacancies_with_higher_salary()

        elif user_choice and user_choice == '5' and user_choice in choice_number:
            user_input = input('введите ключевое слово: ')
            db_man_inst.get_vacancies_with_keyword(user_input)

        elif user_choice and user_choice == '0' and user_choice in choice_number:
            db_man_inst.conn_close()
            break

        else:
            print(f"{'⛔' * 3}Вы ввели неверное значение, попробуйте ещё раз{'⛔' * 3}")


if __name__ == '__main__':
    main()

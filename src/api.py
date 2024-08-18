from abc import ABC, abstractmethod
import requests
from src.vacancy import Vacancy


class Parser(ABC):
    """
    Абстрактный класс для работы с API
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_vacancies(self, page_quantity):
        pass


employers_ids = {
    10259650: 'Softintermob LLC',
    3432635: 'ООО EVOS',
    9196211: 'JFoRecruitment',
    6000512: 'ООО Долсо',
    656481: 'Biglion',
    1577237: 'ООО Эрвез',
    5879545: 'ООО Фаст Софт',
    10882430: 'Лаборатория айти',
    2437802: 'ООО Леон',
    1740: 'Яндекс'
}


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом
    """
    employers_data = employers_ids

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'page': 0,
                       'only_with_salary': True,
                       'per_page': 100}
        self.vacancies = []

    def load_vacancies(self, page_quantity: int = 20) -> None:
        """Загружает данные с АПИ по определенным параметрам"""
        self.params['employer_id'] = self.employers_data
        while self.params['page'] != page_quantity:
            response = requests.get(self.url, headers=self.__headers, params=self.params)
            response.raise_for_status()
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1

    @staticmethod
    def parse_vacancies(vacancies: list[dict]) -> list[object]:
        """
        Метод фильтрует с API по заданным ключам и возвращает список экз. класса
        """
        items = []
        for vacancy in vacancies:
            vacancy_name = vacancy.get('name')
            vacancy_url = vacancy.get('alternate_url')
            salary_dict = vacancy.get('salary')
            salary_from = salary_dict.get('from')
            if salary_from is None:
                salary_from = 0
            if salary_dict:
                salary_dict = vacancy.get('salary')
                currency = salary_dict.get('currency')
            else:
                currency = ''
            snippet_dict = vacancy.get('snippet')
            snippet_requirement = snippet_dict.get('requirement')
            if snippet_requirement:
                snippet_requirement = snippet_requirement.replace('<highlighttext>', '').replace('</highlighttext>', '')
            else:
                snippet_requirement = 'нет требований'
            employer = vacancy.get('employer')
            employer_id = employer.get('id')
            employer_name = employer.get('name')

            vacancy_object = Vacancy(vacancy_name, vacancy_url, salary_from, currency, snippet_requirement,
                                     employer_id, employer_name)
            items.append(vacancy_object)

        return items


from datetime import datetime


class Date_Tools():
    # Transforme un string représentant une date en un objet date
    @staticmethod
    def string_to_date(date_string):
        date_object = datetime.strptime(date_string, '%Y%m%d')
        formatted_date = date_object.strftime('%Y-%m-%d')
        return formatted_date

    # Transforme un objet date en un string représentant une date
    @staticmethod
    def date_to_string(date_date):
        date_string = date_date('%Y%m%d')
        return date_string

from flask import Flask
from faker import Faker
import requests
import csv
import json
app = Flask(__name__)


@app.route('/space/')
def request_number_of_spacemans_from_link(link="http://api.open-notify.org/astros.json"):
    """Return number of spacemans in space in current time

    :param link: Server with space data
    :return: string
    """
    r = requests.get(link)
    return f"На данный момент в космосе {r.json()['number']} космонавтов"


@app.route('/requirements/')
def read_txt_file(file_name="requirements.txt"):
    """Read .txt file and return data from it

    :param file_name: Name of the file
    :return: string
    """
    with open(file_name) as file:
        return file.read()


def csv_file_column_reader(column_name, file_name, data_type):
    """Read column from .csv file and return it in list

    :param column_name: Name of the column that you need to return
    :param file_name: Name of the .csv file that you need to read
    :param data_type: Choose data type in column that you need to return
    :return: column -> list
    """
    column_list = []
    with open(file_name) as file:
        reader = csv.DictReader(file)
        for row in reader:
            column_list.append((data_type(row[column_name])))
        return column_list


def average(iterable_data):
    """Return average;

    :param iterable_data: must be float and iterable
    :return: average from iterable_data
    """
    sum_data = 0
    for height in iterable_data:
        sum_data += height
    return sum_data/len(iterable_data)


def change_inches_in_centimeters(inches):
    """Change inches in centimeters

    :param inches: input
    :return: centimeters
    """
    return inches * 2.54


def change_pounds_in_kg(pounds):
    """Change pounds in kg

    :param pounds: input
    :return: kg
    """
    return pounds * 0.4535923745


@app.route('/mean/')
def average_height_and_weight():
    """Return average height and weight in centimeters and kg from .csv file.

    :return: string
    """
    average_height = change_inches_in_centimeters(average(csv_file_column_reader(' "Height(Inches)"', "hw.csv", float)))
    average_weight = change_pounds_in_kg(average(csv_file_column_reader(' "Weight(Pounds)"', "hw.csv", float)))
    return f"Средний рост = {average_height} сантиметра, средний вес = {average_weight} килограмма."


@app.route('/generate-users/')
def generate_users(number_of_users=100):
    """Return list of generate users

    :param number_of_users: how much users you need to generate
    :return: string
    """
    fake = Faker()
    users_list = []
    for users in range(number_of_users):
        user_and_email = f"{fake.first_name()} {fake.email()}"
        users_list.append(user_and_email)
    return json.dumps(users_list)[1:-1]


if __name__ == "__main__":
    app.run()

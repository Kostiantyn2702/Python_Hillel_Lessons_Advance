from flask import Flask, request
from faker import Faker
import requests
import csv
import json
import utils
import sqlite3
import random


def parse(link: str) -> dict:
    """Returns a dictionary of key-value pairs after the separator.

    Separators:
    ? - the beginning of the text to be processed
    - after the first sign = start of value
    - before the first character = the beginning of the key
    & - go to the next key

    :param link - string with separators
    :return: my_dict - dict
    """
    if not isinstance(link, str) or link.find("=") == -1:
        return {}

    my_dict = {}
    my_string = link[link.find("?") + 1:]
    split_list = my_string.split("&")
    key_value_list = []

    for words in split_list:
        if words.find("=") != -1:
            key_value_list.append(words)

    for words in key_value_list:
        key = words[:words.find("=")]
        value = words[words.find("=") + 1:]

        if not len(key) or not len(value):
            continue
        my_dict[key] = value

    return my_dict


if __name__ == '__main__':
    assert parse('https://example.com/path/to/page?name=ferret&color=purple') == {'name': 'ferret', 'color': 'purple'}
    assert parse('https://example.com/path/to/page?name=ferret&color=purple&') == {'name': 'ferret', 'color': 'purple'}
    assert parse('http://example.com/') == {}
    assert parse('http://example.com/?') == {}
    assert parse('http://example.com/?name=Dima') == {'name': 'Dima'}
    assert parse('http://example.com/?name=Dima&name=Kostia') == {'name': 'Kostia'}
    assert parse('http://example.com/?Dima&Kostia') == {}
    assert parse('http://example.com/?Dima=Kostia?name=bob') == {"Dima": "Kostia?name=bob"}
    assert parse('http://example.com/?&') == {}
    assert parse('http://example.com/?=&name=Kostia') == {"name": "Kostia"}
    assert parse('http://example.com/?=12&name=Kostia') == {"name": "Kostia"}
    assert parse('') == {}
    assert parse(True) == {}


def parse_cookie(my_string: str) -> dict:
    """Returns a dictionary of key-value pairs after the separator.

    Separators:
    - after the first sign = start of value
    - before the first character = the beginning of the key
    ; - end of the key-value pair

    :param my_string - string with separators
    :return: my_dict - dict
    """
    if not isinstance(my_string, str) or my_string.find("=") == -1 or my_string.find(";") == -1:
        return {}

    my_dict = {}
    key_value_list = []
    split_list = my_string.split(";")

    for words in split_list:
        if words.find("=") != -1:
            key_value_list.append(words)

    for words in key_value_list:
        key = words[0: words.find("=")]
        value = words[words.find("=") + 1:]
        if not len(key) or not len(value):
            continue
        my_dict[key] = value
    return my_dict


if __name__ == '__main__':
    assert parse_cookie('name=Dima;') == {'name': 'Dima'}
    assert parse_cookie('') == {}
    assert parse_cookie('name=Dima;age=28;') == {'name': 'Dima', 'age': '28'}
    assert parse_cookie('name=Dima=User;age=28;') == {'name': 'Dima=User', 'age': '28'}
    assert parse_cookie(123) == {}
    assert parse_cookie("key=1;key=2") == {"key": "2"}
    assert parse_cookie("potato=kartoshka") == {}
    assert parse_cookie("figma=tools;key value;") == {'figma': 'tools'}
    assert parse_cookie("figma=tools;;key=value;") == {'figma': 'tools', "key": "value"}
    assert parse_cookie("=;key=value;1=;") == {"key": "value"}
    assert parse_cookie("==;") == {}
    assert parse_cookie("=;") == {}
    assert parse_cookie("1=;") == {}
    assert parse_cookie("=2;") == {}


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
    users_list = [f"{fake.first_name()} {fake.email()}" for users in range(number_of_users)]
    return json.dumps(users_list)[1:-1]


def sqlite_operation(data_base, instructions):
    """
    This function processes SQL instructions
    :param data_base: SQL database name
    :param instructions: Instruction for SQL
    :return: 
    """
    try:
        connection = sqlite3.connect(data_base)
        cursor = connection.cursor()
        cursor.execute(instructions)
        result = cursor.fetchall()

        connection.commit()
    finally:
        connection.close()

    return str(result)


@app.route("/users/list/")
def users_list():
    """
    This function shows user list
    :return:
    """
    instructions = f"SELECT * FROM users;"
    return sqlite_operation("./db.sqlite3", instructions)


@app.route('/users/create/')
def users_create():
    """
    This function create user in user list
    :return:
    """
    first_name = request.args['firstName']
    last_name = request.args['lastName']
    is_student = int(request.args['isStudent'] == 'true')  # true or false
    ID = random.randint(1, 100_000)  # TODO

    instructions = f"INSERT INTO users VALUES ({ID}, '{first_name}', '{last_name}', {is_student});"
    return sqlite_operation("./db.sqlite3", instructions)


@app.route('/phones/list/')
def phones_list():
    """
    This function shows phones list
    :return:
    """
    instructions = f"SELECT * FROM phones;"
    return sqlite_operation("./db.sqlite3", instructions)


@app.route('/phones/create/')
def phones_create():
    """
    This function create phone number in phones list
    :return:
    """
    phone_number = request.args['phoneNumber']
    user_id = request.args['userId']

    instructions = f"INSERT INTO phones VALUES (null, '{phone_number}', '{user_id}');"
    return sqlite_operation("./db.sqlite3", instructions)


@app.route('/users/phones/')
def users_phones():
    """
    This function shows all users with phones
    :return:
    """
    instructions = f"""
        SELECT users.first_name, users.last_name, users.id, phones.value
        FROM users
        INNER JOIN phones ON phones.user_id = users.id;
        """

    return sqlite_operation("./db.sqlite3", instructions)


@app.route('/emails/list/')
def emails_list():
    """
    This function shows emails list
    :return:
    """
    instructions = f"SELECT * FROM emails;"
    return sqlite_operation("./db.sqlite3", instructions)


@app.route('/emails/create/')
def emails_create():
    """
    This function create user email in emails list
    :return:
    """
    email = request.args['email']
    user_id = request.args['userId']

    instructions = f"INSERT INTO emails VALUES (null, '{email}', '{user_id}');"
    return sqlite_operation("./db.sqlite3", instructions)


@app.route('/emails/update/')
def emails_update():
    """
    This function updates users email in email list
    :return:
    """
    new_email = request.args['email']
    user_id = request.args['userId']

    instructions = f"""
                UPDATE emails
                SET value = '{new_email}'
                WHERE user_id = {user_id};
                """
    return sqlite_operation("./db.sqlite3", instructions)


@app.route('/emails/delete/')
def emails_delete():
    """
    This function delete user email from emails list
    :return:
    """
    user_id = request.args['userId']

    instructions = f"""
                DELETE FROM emails
                WHERE user_id = {user_id};
                """
    return sqlite_operation("./db.sqlite3", instructions)


@app.route('/users/emails/')
def users_emails():
    """
    This function shows all users with emails
    :return:
    """
    instructions = f"""
            SELECT users.first_name, users.last_name, users.id, emails.value
            FROM users
            INNER JOIN emails ON emails.user_id = users.id;
            """

    return sqlite_operation("./db.sqlite3", instructions)


if __name__ == "__main__":
    app.run()

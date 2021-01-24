from flask import Flask, request
import utils
import sqlite3
import random


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

import string
import random
import math
import datetime
import time


def generate_password(length: int) -> str:
    """ The function returns a string of random symbols of a given length

    :param length: Integer
    :return: Random symbols
    """
    if not isinstance(length, int):
        raise TypeError("Wrong data type")

    letters = string.ascii_letters
    password = ""

    for letter in range(length):
        password += random.choice(letters)
    return password


key = 2


def encrypt_message(message: str) -> str:
    """ Encrypts a message by key

    :param message: String
    :return: Encrypts string
    """
    if not isinstance(message, str):
        raise TypeError("Wrong data type")

    return ''.join(
        chr(num + key)
        for num in map(ord, message)
    )


def lucky_number(ticket: str) -> bool:
    """ This function calculates the sum of the first three and the last three digits
    from the number and checks if they are equal

    :param ticket: string with length == 6
    :return: Boolian
    """
    if not isinstance(ticket, str) or len(ticket) != 6:
        raise TypeError("Wrong data type")

    sum_one = 0
    sum_second = 0

    for num in ticket[:3]:
        sum_one += int(num)

    for num in ticket[3:]:
        sum_second += int(num)

    return sum_one == sum_second


def fizz_buzz(num: int) -> str:
    """ This function returns a phrase with the following parameters
    1. If the number is a multiple of three and five - return FizzBuzz
    2. If the number is a multiple of five - return Buzz
    3. If the number is a multiple of three - return Fizz
    4. Else - return num in string

    :param num: Integer
    :return: String
    """
    if not isinstance(num, int):
        raise TypeError("Wrong data type")

    if not num % 3 and not num % 5:
        return "FizzBuzz"
    elif not num % 5:
        return "Buzz"
    elif not num % 3:
        return "Fizz"
    else:
        return str(num)


def password_is_strong(password: str) -> bool:
    """ This function checks the strength of the password against the following parameters:
    1. Has number
    2. Has lowercase char
    3. Has uppercase char
    4. Password length >= 10

    :param password: String
    :return: Boolian
    """
    if not isinstance(password, str):
        raise TypeError("Wrong data type")

    if len(password) < 10 \
            or password.isdigit() \
            or password.islower() \
            or password.isupper() \
            or password.isspace():
        return False
    elif len(password) >= 10 and password.isalnum():
        return True
    else:
        return False


def number_is_prime(num: int) -> bool:
    """ This function determines if the number is prime

    :param num: Integer
    :return: Boolian
    """
    if not isinstance(num, int):
        raise TypeError("Wrong data type")

    if num == 1:
        return False

    generator = [i for i in range(2, num - 1)]

    for number in generator:
        if not num % number:
            return False

    return True


def decrypt_message(message: str) -> str:
    """ This function decrypts the message by key

    :param message: Encrypted message using a similar key
    :return: Message
    """
    if not isinstance(message, str):
        return "Wrong data type"

    return ''.join(
        chr(num - key)
        for num in map(ord, message)
    )


def volume_of_sphere(radius: float) -> float:
    """ This function calculates the volume of a sphere and rounds the value to two decimal places

    :param radius: Sphere radius
    :return: Sphere Volume
    """
    if not isinstance(radius, float):
        raise TypeError("Wrong data type")

    return float('%.2f' % ((4/3)*math.pi*math.pow(radius, 3)))


def days_diff(start_date: ..., end_date: ...) -> int:
    """ The function calculates the difference in days between dates

    :param start_date: YYYY-M-D
    :param end_date: YYYY-M-D
    :return: integer (days)
    """
    if not isinstance(start_date, str) and not isinstance(end_date, str):
        raise TypeError("Wrong data type")

    start_date = time.strptime(start_date,"%Y-%m-%d")
    end_date = time.strptime(end_date,"%Y-%m-%d")

    start_date = datetime.date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    end_date = datetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))

    result = start_date - end_date
    return int(math.fabs(result.days))


def prs(client_choice: str) -> bool:
    """ This function takes one of the values from the client [paper, rock, scissors]
    and generates a random value from the same list.

    :param client_choice: string - paper, rock or scissors
    :return: True or False depending on the condition ... > rock > scissors > paper > rock > scissors > ...
    """
    if not isinstance(client_choice, str):
        raise TypeError("Wrong data type")

    if client_choice not in ("paper", "rock", "scissors"):
        raise TypeError("Wrong atribute")

    enemy_choice = random.choice(["paper", "rock", "scissors"])

    if client_choice == enemy_choice:
        return False
    elif client_choice == "paper" and enemy_choice == "scissors":
        return False
    elif client_choice == "scissors" and enemy_choice == "rock":
        return False
    elif client_choice == "rock" and enemy_choice == "paper":
        return False

    return True


def integer_as_roman(integer: int) -> str:
    """ This function converts Arabic numbers to Roman numbers in the range 1 to 3999

    :param integer: integer
    :return: roman number
    """
    if not isinstance(integer, int):
        raise TypeError("Wrong data type")

    roman = ""
    roman_numbers_dict = {1: "I", 5: "V", 10: "X", 50: "L", 100: "C", 500: "D", 1000: "M"}

    if integer in range(1, 4000):
        string_integer = str(integer)
        counter = 0

        while counter < len(string_integer):
            zero_multiplier = "0" * (len(string_integer[counter:]) - 1)
            multiplier = int("1" + zero_multiplier)

            from_one_to, four = (int("1" + zero_multiplier), int("4" + zero_multiplier))
            from_four_to, five = (int("4" + zero_multiplier), int("5" + zero_multiplier))
            from_five_to, nine = (int("5" + zero_multiplier), int("9" + zero_multiplier))
            from_nine_to, ten = (int("9" + zero_multiplier), int("10" + zero_multiplier))

            if int(string_integer[counter:]) in range(from_one_to, four):

                for i in range(int(string_integer[counter])):
                    roman += roman_numbers_dict[multiplier]

            elif int(string_integer[counter:]) in range(from_four_to, five):
                roman += roman_numbers_dict[multiplier]
                roman += roman_numbers_dict[five]

            elif int(string_integer[counter:]) in range(from_five_to, nine):
                roman += roman_numbers_dict[from_five_to]
                diapason = int((string_integer[counter:])[0]) - int(str(from_five_to)[0])

                for i in range(int(diapason)):
                    roman += roman_numbers_dict[multiplier]

            elif int(string_integer[counter:]) in range(from_nine_to, ten):
                roman += roman_numbers_dict[multiplier]
                roman += roman_numbers_dict[ten]

            counter += 1

        return roman

    else:
        return "Out of range!"


if __name__ == '__main__':
    assert len(generate_password(5)) == 5
    assert len(generate_password(10)) == 10
    assert len(generate_password(24)) == 24
    assert len(generate_password(5)) != 4
    assert type(generate_password(5)) == str

    assert encrypt_message('Dima') == 'Fkoc'
    assert encrypt_message('Kostia') == 'Mquvkc'
    assert encrypt_message('Bugsnax') == 'Dwiupcz'
    assert encrypt_message('Hello World!') == 'Jgnnq"Yqtnf#'
    assert type(encrypt_message('Bugsnax')) == str

    assert lucky_number("667766") == True
    assert lucky_number("111111") == True
    assert lucky_number("000000") == True
    assert lucky_number("123456") == False
    assert type(lucky_number("123456")) == bool

    assert fizz_buzz(15) == "FizzBuzz"
    assert fizz_buzz(30) == "FizzBuzz"
    assert fizz_buzz(18) == "Fizz"
    assert fizz_buzz(25) == "Buzz"
    assert fizz_buzz(13) == "13"

    assert password_is_strong("12345678Da") == True
    assert password_is_strong("1234567890") == False
    assert password_is_strong("12345Da") == False
    assert password_is_strong("&&&&&&&&&&") == False
    assert password_is_strong("yfugwuy32674896>V>") == False

    assert number_is_prime(2) == True
    assert number_is_prime(1) == False
    assert number_is_prime(45) == False
    assert number_is_prime(67) == True
    assert number_is_prime(75) == False

    assert decrypt_message('Fkoc') == 'Dima'
    assert decrypt_message('Mquvkc') == 'Kostia'
    assert decrypt_message('Dwiupcz') == 'Bugsnax'
    assert decrypt_message('Jgnnq"Yqtnf#') == 'Hello World!'
    assert type(decrypt_message('WDiuhf')) == str

    assert type(prs("paper")) == bool
    assert type(prs("scissors")) == bool
    assert type(prs("rock")) == bool

    assert volume_of_sphere(10.0) == 4188.79
    assert volume_of_sphere(10.0) != 4188.7902
    assert type(volume_of_sphere(10.0)) == float
    assert volume_of_sphere(5.5) == 696.91
    assert volume_of_sphere(20.0) == 33510.32

    assert days_diff("2021-1-5", "2021-1-1") == 4
    assert days_diff("2021-01-05", "2021-01-01") == 4
    assert days_diff("2021-1-5", "2020-1-5") == 366
    assert days_diff("2020-1-5", "2021-1-5") == 366
    assert days_diff("2021-1-10", "2021-1-10") == 0

    assert integer_as_roman(1) == 'I'
    assert integer_as_roman(2) == 'II'
    assert integer_as_roman(3) == 'III'
    assert integer_as_roman(4) == 'IV'
    assert integer_as_roman(5) == 'V'
    assert integer_as_roman(6) == 'VI'
    assert integer_as_roman(7) == 'VII'
    assert integer_as_roman(8) == 'VIII'
    assert integer_as_roman(9) == 'IX'
    assert integer_as_roman(10) == 'X'
    assert integer_as_roman(50) == 'L'
    assert integer_as_roman(89) == 'LXXXIX'
    assert integer_as_roman(95) == 'XCV'
    assert integer_as_roman(100) == 'C'
    assert integer_as_roman(500) == 'D'
    assert integer_as_roman(999) == 'CMXCIX'
    assert integer_as_roman(1000) == 'M'
    assert integer_as_roman(1514) == 'MDXIV'
    assert integer_as_roman(2471) == 'MMCDLXXI'
    assert integer_as_roman(3259) == 'MMMCCLIX'
    assert integer_as_roman(3690) == 'MMMDCXC'
    assert integer_as_roman(3999) == 'MMMCMXCIX'
    assert integer_as_roman(4000) == "Out of range!"

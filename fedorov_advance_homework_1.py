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

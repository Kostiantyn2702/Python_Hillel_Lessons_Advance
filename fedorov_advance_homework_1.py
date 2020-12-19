# На каком-нибудь PyCheckio сидит чувак который может написать это в одну строчку, но это не я.
def parse(link: str) -> dict:
    if type(link) != str or link.find("=") == -1:
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
        if len(key) == 0 or len(value) == 0:
            continue
        my_dict[key] = value
    return my_dict

if __name__ == '__main__':
    assert parse('https://example.com/path/to/page?name=ferret&color=purple') == {'name': 'ferret', 'color': 'purple'}
    assert parse('https://example.com/path/to/page?name=ferret&color=purple&') == {'name': 'ferret', 'color': 'purple'}
    assert parse('http://example.com/') == {}
    assert parse('http://example.com/?') == {}
    assert parse('http://example.com/?name=Dima') == {'name': 'Dima'}
    # Ломал как мог
    assert parse('http://example.com/?name=Dima&name=Kostia') == {'name': 'Kostia'}
    assert parse('http://example.com/?Dima&Kostia') == {}
    assert parse('http://example.com/?Dima=Kostia?name=bob') == {"Dima": "Kostia?name=bob"}
    assert parse('http://example.com/?&') == {}
    assert parse('http://example.com/?=&name=Kostia') == {"name": "Kostia"}
    assert parse('http://example.com/?=12&name=Kostia') == {"name": "Kostia"}
    assert parse('') == {}
    assert parse(True) == {}

def parse_cookie(my_string: str) -> dict:
    if type(my_string) != str or my_string.find("=") == -1 or my_string.find(";") == -1:
        return {}
    my_dict = {}
    key_value_list = []
    split_list = my_string.split(";")
    for words in split_list:
        if words.find("=") != -1:
            key_value_list.append(words)
    for words in key_value_list:
        key = words[0 : words.find("=")]
        value = words[words.find("=") + 1 : ]
        if len(key) == 0 or len(value) == 0:
            continue
        my_dict[key] = value
    return my_dict

if __name__ == '__main__':
    assert parse_cookie('name=Dima;') == {'name': 'Dima'}
    assert parse_cookie('') == {}
    assert parse_cookie('name=Dima;age=28;') == {'name': 'Dima', 'age': '28'}
    assert parse_cookie('name=Dima=User;age=28;') == {'name': 'Dima=User', 'age': '28'}
# Ломал как мог
    assert parse_cookie(123) == {}
    assert parse_cookie("key=1;key=2") == {"key": "2"}
    assert parse_cookie("potato=kartoshka") == {} # Приянл что символ ; обязателен для обозначения конца пары(ключ-значение) так как по поводу этого условий небыло
    assert parse_cookie("figma=tools;key value;") == {'figma': 'tools'}
    assert parse_cookie("figma=tools;;key=value;") == {'figma': 'tools',"key": "value"}
    assert parse_cookie("=;key=value;1=;") == {"key": "value"}
    assert parse_cookie("==;") == {}
    assert parse_cookie("=;") == {}
    assert parse_cookie("1=;") == {}
    assert parse_cookie("=2;") == {}



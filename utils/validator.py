import re


def mobile(text):
    return re.match('^1[3-9]\d{9}$', text)


def email(text):
    return re.match('^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9_-]+$]', text)


def while_input(text, validator=None):
    while True:
        data = input(text).strip()
        if not data:
            print('输入不能为空')
            continue
        if not validator:
            return data
        if not validator(data):
            print('格式错误')
            continue
        return data


if __name__ == '__main__':
    t = email('123@qq.com')
    print(t)
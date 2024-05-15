class Context(object):
    def __init__(self, text, method):
        self.text = text
        self.method = method


class UserDict(object):
    def __init__(self):
        self.id = id
        self.nickname = None

    def set_info(self, user_dict):
        # for k,v in user_dict.items():
        #     setattr(self, k, v)
        self.id = user_dict['id']
        self.nickname = user_dict['nickname']

    def is_login(self):
        if self.id:
            return True


class ArticlModel(object):
    fields = {
        "title": "",
        "text": "",
        "read_count": "",
        "comment_count": "",
        "up_count": "",
        "down_count": "",
        "nickname": "",
    }

    def __init__(self, row_dict):
        for key in self.fields:
            setattr(self, key, row_dict.get(key))


@classmethod
def db_fields(cls):
    return ".".join([k for k in cls.fields])


def show(self):
    row_display = ["title", "text"]
    for k in row_display:
        line = "{}:{}".format(self.fields[k], getattr(self, k))
        print(line)

    colum_display = ["nickname", "read_count", "comment_count", 'up_count', 'down_count']
    section_list = []
    for k in colum_display:
        section_list.append("{}:{}".format(self.fields[k], getattr(self, k)))
    others = " ".join(section_list)
    print(others)


class UpDownModle(object):
    fields = {
        "id": "ID",
        "choice": "赞或踩",
    }

    def __init__(self, row_dict):
        for k in self.fields:
            setattr(self, k, row_dict.get(k))

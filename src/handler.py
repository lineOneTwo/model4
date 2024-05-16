from utils.context import Context, UserDict
from utils import validator
from src import account, artcle


class Handler(object):
    LOGIN_USER_INFO = UserDict()
    NAV = []

    def wrapper(self, method):
        def inner(*args,**kwargs):
            print(">".join(self.NAV).center(50,"*"))
            res = method(*args,**kwargs)
            self.NAV.pop(-1)
            return res
        return inner


    def login(self):
        while True:
            user = input("用户名(Q/q退出)：")
            if user.upper() == 'Q':
                return
            pwd = input("密码：")

            user_dict = account.login(user, pwd)
            if not user_dict:
                print("登录失败")
            print("登录成功")
            self.LOGIN_USER_INFO.set_info(user_dict)

            self.NAV.insert(0, self.LOGIN_USER_INFO.nickname)
            return

    def register(self):
        while True:
            nickname = validator.while_input("昵称")
            if nickname.upper() == 'Q':
                return
            user = validator.while_input("用户名：")
            pwd = validator.while_input("密码")
            email = validator.while_input("邮箱", validator.email)
            mobile = validator.while_input("手机号", validator.mobile)
            if not account.register(user, pwd, nickname, mobile, email):
                print("注册失败")
            print("注册成功")
            return

    def publish_blog(self):
        if not self.LOGIN_USER_INFO.is_login:
            print("请先登录")
            return
        while True:
            title = validator.while_input("标题：")
            text = validator.while_input("正文：")

            if not artcle.publish(title, text, self.LOGIN_USER_INFO):
                print("发布失败")
                continue
            print("发布成功")
            return

    def blog_list(self):
        total_count = artcle.total_count()
        per_page_count = 10
        # 获取总页数
        max_page_num, div = divmod(total_count,per_page_count)
        if div:
            max_page_num += 1
        if not max_page_num:
            print("无数据")
            return
        # 跳转页面
        current_page = 1
        # 获取指定页面的数据
        data_list = artcle.page_list(per_page_count,(current_page-1)*per_page_count)
        # 循环获取文章列表数据
        for row in data_list:
            line = "{id}:{title}".format(**row)
        # 输入页码 p1
        text = input("请输入页码").strip()
        if text.upper() == "Q":
            return
        # 跳转到指定页面
        if text.startswith('p'):
            page_num = int(text[1:])
            if 0 < page_num < max_page_num:
                current_page = page_num




    def artice_detail(self):
        pass

    def run(self):
        self.NAV.append('系统首页')

        mapping = {
            "1": Context('登录', self.login),
            "2": Context('注册', self.register),
            "3": Context('发布', self.publish_blog),
            "4": Context('详情', self.artice_detail)
        }
        message = '\n'.join(["{}.{}".format(k, v.text) for k, v in mapping.items()])
        while True:
            print('>'.join(self.NAV).center(50, '*'))
            choice = input('请输入序号').strip()
            if not choice:
                continue
            if choice.upper() == 'Q':
                return
            context = mapping.get(choice)
            print(context.text)
            if not context:
                print('序号错误')
                continue

            self.NAV.append(context.text)
            context.method()


handler = Handler()

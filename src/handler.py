from utils.context import Context, UserDict
from utils import validator
from src import account


class Handler(object):
    LOGIN_USER_INFO = UserDict()
    NAV = []

    def login(self):
        pass

    def register(self):
        while True:
            nickname = validator.while_input("昵称")
            if nickname.upper() == 'Q':
                return
            user = validator.while_input("用户名：")
            pwd = validator.while_input("密码")
            email = validator.while_input("邮箱", validator.email)
            mobile = validator.while_input("手机号", validator.mobile)
            if not account.register(user,pwd,nickname,mobile,email):
                print("注册失败")
            print("注册成功")
            return
    def publish_blog(self):
        pass

    def blog_list(self):
        pass

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

from utils.context import Context, UserDict
from utils import validator
from src import account, artcle


class Handler(object):
    LOGIN_USER_INFO = UserDict()
    NAV = []

    def wrapper(self, method):
        def inner(*args, **kwargs):
            print(">".join(self.NAV).center(50, "*"))
            res = method(*args, **kwargs)
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
        max_page_num, div = divmod(total_count, per_page_count)
        if div:
            max_page_num += 1
        if not max_page_num:
            print("无数据")
            return
        # 跳转页面
        current_page = 1

        counter = 0
        while True:
            # 获取指定页面的数据
            data_list = artcle.page_list(per_page_count, (current_page - 1) * per_page_count)
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
                continue
            # 查看文章详情
            if not text.isdecimal():
                print("格式错误，请重新输入")
                continue
            article_id = int(text)
            # 根据文章id获取文章内容
            article_object = artcle.get_article(article_id)
            if not article_object:
                print("文章不存在")
                continue
            # 增加标题内容
            self.NAV.append("文章详情")
            self.wrapper(self.artice_detail)(article_id, article_object)

    def artice_detail(self, artice_id, article_object):
        article_object.show()
        artcle.update_read_count(artice_id)

        def up():
            # 查询当前用户对文章的踩赞记录
            up_down_object = artcle.fetch_up_down(self.LOGIN_USER_INFO.id, artice_id)
            if not up_down_object:
                # 当前用户点赞
                if artcle.up(self.LOGIN_USER_INFO.id, artice_id):
                    print("点赞成功")
                else:
                    print("点赞失败")
            if up_down_object.choice == 1:
                print("已赞过，不能重复操作")
                return
            if artcle.update_doown_to_up(artice_id, up_down_object.id):
                print("点赞成功")
            else:
                print("点赞失败")

        def down():
            up_down_object = artcle.fetch_up_down(self.LOGIN_USER_INFO.id, artice_id)
            if not up_down_object:
                if artcle.down(self.LOGIN_USER_INFO.id, artice_id):
                    print("踩成功")
                else:
                    print("踩失败")
                return
            if up_down_object.choice == 0:
                print("已踩过，不能重复操作")
                return
            if artcle.update_doown_to_up(artice_id, up_down_object.id):
                print("踩成功")
            else:
                print("踩失败")

        def comment():
            comment_text = input("请输入评论内容")
            if artcle.comment(self.LOGIN_USER_INFO.id, artice_id, comment_text):
                print("评论成功")
            else:
                print("评论失败")

        mapping = {
            "1":Context("赞",up),
            "2":Context("踩",down),
            "3":Context("评论",comment)

        }
        message = ";".join(["{}.{}".format(k,v.text) for k,v in mapping.items()])
        message = "\n提示：{}".format(message)
        while True:
            print(message)
            choice = input("请输入Q/q退出：").strip()
            if choice.upper() == "Q":
                break
            if not self.LOGIN_USER_INFO.is_login:
                print("用户未登录，无法进行赞、踩、评论")
                return
            if not choice:
                continue
            ctx = mapping.get(choice)
            if not ctx:
                print("输入错误")
                continue
            ctx.method()
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

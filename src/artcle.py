import datetime
from utils.db import Connect
from utils.context import ArticlModel, UpDownModle


def publish(title, text, user_id):
    try:
        with Connect() as conn:
            sql = 'insert into article(title,text,user_id) values(%s,%s,%s,%s)'
            result = conn.exce(sql, title, text, user_id, datetime.datetime.now())
            return result
    except:
        print("文章发布失败")


def total_count():
    with Connect() as conn:
        sql = "select count(1) as ct from article"
        result = conn.fetch_one(sql)
        if not result:
            return 0
        return result['ct']


def page_list(limit, offset):
    with Connect() as conn:
        sql = "select id,title from article order by id desc limit %s offset %s"
        result = conn.fetch_all(sql, limit, offset)
        return result


def get_article(aid):
    with Connect() as conn:
        sql = "select {} from article left join user on article.user_id = user_id where article.id = %s".format(
            ArticlModel.db_fields())
        result = conn.fetch_one(sql, aid)
        if not result:
            return None
        return ArticlModel(result)


def update_read_count(aid):
    with Connect() as conn:
        sql = 'update article set read_count=read_count+1 where id=%s'
        result = conn.exce(sql, aid)
        return result


def fetch_up_down(user_id, aid):
    with Connect() as conn:
        sql = "select id ,choice from up_dwown where user_id=%s and article_id=%s"
        result = conn.fetch_one(sql, user_id, aid)
        if result:
            return UpDownModle(result)


def up(user_id, aid):
    with Connect() as conn:
        conn.conn.begin()
        try:
            sql = "insert into up_down(user_id,article_id,choice_id,ctime) values(%s,%s,1,%s)"
            result = conn.cursor.execute(sql, [user_id, aid, datetime.datetime.now()])
            up_sql = "update article set up_count=up_count+1 where id=%s"
            conn.cursor.execute(up_sql, [aid])
            conn.conn.commit()
            return True
        except Exception as e:
            conn.conn.rollback()

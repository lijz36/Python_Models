import pymysql
from pymongo import MongoClient
import gridfs
from .lijzLog import *


def __singletion(cls):
    """
    单例模式的装饰器函数
    :param cls: 实体类
    :return: 返回实体类对象
    """
    instances = {}
    def getInstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getInstance


@__singletion
class C_MySQLHelper(object):
    def __init__(self, host=None, user=None, pwd=None, db=None, charset='utf8'):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.charset = charset
        self.logger = C_Logger('lijzMySQL', 'lijzMySQL.log', out=1).getLogger()

    # 连接数据库
    def __connectDB(self):
        try:
            config = {
                "host": self.host,
                'user': self.user,
                'pwd': self.pwd,
                'db': self.db,
                'charset': self.charset
            }
            self.conn = pymysql.connect(**config)
        except:
            self.logger.error("连接数据库失败！")
            return False
        self.cursor = self.conn.cursor()
        return True

    # 执行数据库的SQL语句,主要用来做插入
    def __execute(self, sql, params=None):
        self.__connectDB()
        try:
            if self.conn and self.cursor:
                # 正常逻辑，执行sql,并提交
                self.cursor.execute(sql, params)
                self.conn.commit()
        except:
            # 如果有事务是，可以使用回滚操作
            # self.conn.rollback()
            self.logger.error("Execute Failed:" + sql)
            self.logger.error("params:" + params)
            self.__close()
            return False
        finally:
            self.__close()
        return True

    # 用来查询数据
    def fetchall(self, sql, params=None):
        if self.__execute(sql, params):
            return self.cursor.fetchall()
        return None

    # 用来查询一条数据
    def fetchone(self, sql, params=None):
        if self.__execute(sql, params):
            return self.cursor.fetchone()
        return None

    def __close(self):
        # 如果数据库打开就关闭，否则无操作
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
        return True


@__singletion
class mongohelper(object):
    """MongoDB数据库管理操作类"""
    def __init__(self, host, port, db, collection):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection
        self.conn = MongoClient(self.host, self.port)

    def create_obj(self):
        self.obj = self.conn[self.db][self.collection]

    def create_fs(self):
        dbs = self.conn.grid
        self.fs = gridfs.GridFS(dbs)

    def insert(self, sql):
        self.create_obj()
        self.obj.insert(sql)
        self._close()

    def update(self, sql):
        self.create_obj()
        self.obj.update(sql)
        self._close()

    def remove(self, sql):
        self.create_obj()
        self.obj.remove(sql)
        self._close()

    def find(self, sql):
        self.create_obj()
        self.obj.find(sql)
        self._close()

    def find_files(self, filename):
        try:
            files = self.fs.find()
            if files.count() > 0:
                for file in files:
                    if file.filename == filename:
                        with open(file.filename, 'wb') as f:
                            while True:
                                data = file.read(128)
                                if not data:
                                    break
                                f.write(data)
        except Exception as e:
            print(e)
        finally:
            self._close()

    def _close(self):
        self.conn.close()
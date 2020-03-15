import MySQLdb

class Model(object):

    def __init__(self,host='127.0.0.1',username="root",password="123456",db="test"):
        """
        :param host:主机IP
        :type host :str
        :param username:账号
        :type username:str
        :param password:密码
        :type password:str
        :param db:数据库名
        :type db:str
        """
        self.db = MySQLdb.connect(host,username,password,db,charset="utf8")
        self.cursor = self.db.cursor()

    def execute(self,sql):
        """
        :param sql:sql语句
        :type sql:str
        """
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def addData(self,column,data,table):
        """
        :param column:字段
        :type column:list
        :param data:向字段添加的数据
        :type data:list
        :param table:数据库表
        :type table:str
        """
        columnstr = ",".join(column)
        datastr = "','".join(data)
        sql = "insert into " + table + " ("+ columnstr +") values ('" + datastr +"');"
        self.execute(sql)

    def deleteData(self,where,table):
        """
        :param where:删除条件
        :type where:str
        :param table:删除的表
        :type table:str
        """
        sql = "delete from " + table + " where " + where + ";"
        self.execute(sql)


    def updateData(self,setstr,where,table):
        """
        :param setstr:更新的内容
        :type setstr:str
        :param where:更新的位置
        :type where:str
        :param table:更新的表
        :type table:str
        """
        sql = "update " + table +" set "+ setstr + " where " + where + ";"
        self.execute(sql)

    def selectData(self,table):
        """
        :param table:表名
        :type table:str
        """
        sql = "select * from " + table +";"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def __del__(self):
        self.db.close()
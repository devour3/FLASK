# @Version : 1.0
# @Author : fm
from flask import Blueprint, render_template, request, redirect, jsonify
from sqlalchemy.testing.pickleable import User
from functools import wraps
from ..models.models_admin import *
from ..models.models import *
import time
# 蓝图
admin = Blueprint('admin', __name__)
#----------后台管理------------
#装饰器：登陆验证
def login_required(fn):

    @wraps(fn)

    def inner(*args, **kwargs):
        # 判断用户登录
        # 获取cookie，得到登录用户
        user_id =request.cookies.get('user_id',None)
        if user_id:
            user = AdminUserModel.query.get(user_id)
            request.user = user
            return fn(*args, **kwargs)
        else:
            return redirect('/admin/login/')
    return inner
@admin.route('/admin/')
@admin.route('/admin/index/')
@login_required
def index():
    #获取cookie，得到登录的用户
    # user_id = request.cookies.get('user_id',None)
    # if user_id:
    #     user = AdminUserModel.query.get(user_id)
    # else:
    #     #跳转到登录页面
    #     return render_template('admin/login.html/')

    user = request.user
    categorys = CategoryModel.query.filter()
    articles = ArticleModel.query.filter()
    photos = PhotoModel.query.filter()
    return render_template('admin/index.html',
                           username=user.name
                           , categorys=categorys,
                           articles=articles,
                           photos=photos)
#后台管理
@admin.route('/admin/login/',methods=['GET','POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/login.html')

    elif request.method == 'POST':

        username = request.form.get('username')
        userpwd = request.form.get('userpwd')

        user =AdminUserModel.query.filter_by(name=username,passwd = userpwd).first()
        if user:

            pass
            response = redirect('/admin/index/')
            response.set_cookie('user_id',str(user.id),max_age=7*24*3600)
            return response
        else:
            return 'login failed'
#后台管理退出登录
@admin.route('/admin/logout/',methods=['GET','POST'])
def admin_logout():
    response = redirect('/admin/login/')
    response.delete_cookie('user_id')
    return response

#-----------------分类管理-------------------
#后台管理-分类管理
@admin.route('/admin/category/',methods=['GET','POST'])
@login_required
def admin_category():
    user = request.user
    categorys = CategoryModel.query.all()
    return render_template('admin/category.html',
                           username = user.name,
                           categorys=categorys)

#后台管理添加分类
@admin.route('/admin/addcategory/',methods=['GET','POST'])
@login_required
def admin_add_category():
    if request.method == 'POST':
        #添加分类
        name = request.form.get('name')
        describe = request.form.get('describe')

        #添加分类

        category = CategoryModel()
        category.name = name
        category.describe = describe

        try:
            db.session.add(category)
            db.session.commit()
        except Exception as e:
            print('e:',e)
            db.session.rollback()

        return redirect('/admin/category/')
    else:
        return '请求方式错误'

#后台管理删除操作
@admin.route('/admin/delcategory/',methods=['GET','POST'])
@login_required
def admin_del_category():
    if request.method == 'POST':

        #删除分类
        id = request.form.get('id')
        category = CategoryModel.query.get(id)

        try:
            db.session.delete(category)
            db.session.commit()
        except Exception as e:
            print('e:',e)


        return jsonify({'code':200,'msg':'删除成功！'})
    else:
        return jsonify({'code':400,'msg':'请求错误！'})

#后台管理——修改分类

@admin.route('/admin/updatecategory/<id>/',methods=['GET','POST'])
@login_required
def admin_update_category(id):

    if request.method == 'GET':
        user = request.user
        category = CategoryModel.query.get(id)
        return render_template('admin/category_update.html',
                               username = user.name,
                               category = category)

    elif request.method == 'POST':
        name = request.form.get('name')
        describe = request.form.get('describe')

        #修改

        category = CategoryModel.query.get(id)
        category.name = name
        category.describe = describe
        try:
            db.session.commit()
        except Exception as e:
            print('e:',e)
        return redirect('/admin/category/')
    else:
        return '请求方式错误'


#----------文章管理----------
@admin.route('/admin/article/')
@login_required
def admin_article():
    user = request.user
    articles = ArticleModel.query.all()
    categorys = CategoryModel.query.all()
    return render_template('admin/article.html',
                           username = user.name,
                           articles=articles)

#---------添加文章——————————————

@admin.route('/admin/addarticle/',methods=['GET','POST'])
@login_required
def admin_add_article():
    if request.method == 'GET':
        user = request.user
        categorys = CategoryModel.query.all()

        return render_template('admin/article_add.html',
                               username = user.name,
                               categorys=categorys)
    elif request.method == 'POST':

        name = request.form.get('name')
        keywords = request.form.get('keywords')
        content = request.form.get('content')
        category = request.form.get('category')
        img = request.files.get('img')
        # print('img' ,img)
        # print('img.filename',img.filename)

        #添加文章只有图片是存路径
        img_name = f'{time.time()}-{img.filename}'
        img_url = f'/static/home/uploads/{img_name}'

        #
        try:
            atricle =ArticleModel()
            atricle.name =name
            atricle.keyword =keywords
            atricle.content =content
            atricle.img = img_url  #图片的路径
            atricle.category_id = category

            db.session.add(atricle)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            print('e:',e)
        else:
            #如果添加数据库
            img_data = img.read()
            with open(f'App/{img_url}', 'wb') as fp:
                fp.write(img_data)
                fp.flush()

        return redirect('/admin/article/')
#修改文章
@admin.route('/admin/updatearticle/',methods=['GET','POST'])
@login_required
def add_update_article():
    user = request.user
    articles = ArticleModel.query.all()
    return render_template('admin/article_update.html',
                           username = user.name,
                           articles=articles)

#删除文章
@admin.route('/admin/delarticle/',methods=['GET','POST'])
@login_required
def admin_del_article():
    if request.method == 'POST':

        # 删除分类
        id = request.form.get('id')
        article = ArticleModel.query.get(id)

        try:
            db.session.delete(article)
            db.session.commit()
        except Exception as e:
            print('e:', e)
            return jsonify({'code': 500, 'msg': '删除失败！'})

        return jsonify({'code': 200, 'msg': '删除成功！'})

    return jsonify({'code': 400, 'msg': '请求错误！'})

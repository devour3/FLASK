from flask import Blueprint,render_template,request
from ..models.models import *

# 蓝图
blog = Blueprint('blog', __name__)

#博客的首页
@blog.route('/')
@blog.route('/index/')
def blog_index():
    photos = PhotoModel.query.limit(6)
    categories = CategoryModel.query.all
    return render_template('home/index.html',
                           photos = photos
                           ,categories = categories)
#博客-我的相册
@blog.route('/photos/')
def blog_photos():
    return render_template('home/photos.html')
# 我的日记

@blog.route('/article/')
def blog_article():
    return render_template('home/article.html')

#关于我
@blog.route('/about/')
def blog_about():
    return render_template('home/about.html')

import datetime
from datetime import time

from flask import Blueprint, render_template, request, g, current_app, session

from App.exts import cache
from App.models import *

blue2 = Blueprint('admin', __name__)


# 首页
@blue2.route('/admin/')
def index():
    username = session.get('username', '')
    if username == '':
        return render_template('admin/login.html')
    return render_template('admin/index.html')

# 登录
@blue2.route('/admin/login/', methods=['GET', 'POST'])
def login():
    # session.pop('username')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('userpwd')
        print('*'*50)
        if username=='admin' and password == '123456':
            session['username'] = username
            return render_template('admin/index.html', username=username)
        return "用户名或密码错误"
    return render_template('admin/login.html')

# 退出登录
@blue2.route('/admin/logout/')
def abort():
    session.clear()
    return render_template('admin/login.html')

@blue2.route('/admin/article/')
def get_article():
    username = session.get('username', '')
    if username == '':
        return render_template('admin/login.html')
    articles = Article.query.all()
    categories = Category.query.all()
    return render_template('admin/article.html', articles=articles, categories=categories)

@blue2.route('/admin/notice/')
def get_notice():
    username = session.get('username', '')
    if username == '':
        return render_template('admin/login.html')
    return render_template('admin/notice.html')

@blue2.route('/admin/comment/')
def get_comment():
    username = session.get('username', '')
    if username == '':
        return render_template('admin/login.html')
    return render_template('admin/comment.html')

# 显示和添加类别
@blue2.route('/admin/category/', methods=['GET', 'POST'])
def get_category():
    username = session.get('username', '')
    categories = Category.query.all()
    if username == '':
        return render_template('admin/login.html')
    if request.method == "POST":
        # 如果是提交表单，则获取相关内容
        category = Category()
        category.name = request.form.get('name')
        category.alias = request.form.get('alias')
        category.count = 0
        try:
            db.session.add(category)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        categories = Category.query.all()
        return render_template('admin/category.html', categories=categories)
    return render_template('admin/category.html', categories=categories)

# 修改类别
@blue2.route('/admin/updateCategory/<int:cid>/', methods=['GET', 'POST'])
def update_category(cid):
    category = Category.query.get(cid)
    username = session.get('username')
    if username == '':
        return render_template('admin/login.html')
    if request.method == 'POST':
        # 如果提交表单，则在此处修改类别
        # category = Category.query.get(cid)
        category.name = request.form.get("name")
        category.alias = request.form.get("alias")
        try:
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        categories = Category.query.all()
        return render_template('admin/category.html',categories=categories)
    return render_template('admin/update-category.html',category=category)

@blue2.route('/admin/deleteCategory/<int:cid>/')
def delete_category(cid):
    username = session.get('username')
    if username == '':
        return render_template('admin/login.html')
    category = Category.query.get(cid)
    db.session.delete(category)
    db.session.commit()
    db.session.flush()
    # 删除分类也会删除分类下的所有文章
    articles = category.articles
    for article in articles:
        db.session.delete(article)
        db.session.commit()
    categories = Category.query.all()
    return render_template('admin/category.html', categories=categories)

@blue2.route('/admin/addArticle/',methods=["GET", 'POST'])
def add_article():
    username = session.get('username', '')
    if username == '':
        return render_template('admin/login.html')

    categories = Category.query.all()
    if request.method == "POST":
        article = Article()
        article.title = request.form.get("title")
        article.text = request.form.get("content")
        article.tags = request.form.get("tags")
        article.comment_count = 0
        article.category_id = request.form.get("category")
        article.date = datetime.datetime.now()
        checkbox = request.form.get('checkbox[]')
        print(checkbox)
        try:
            db.session.add(article)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        articles = Article.query.all()
        categories = Category.query.all()
        return render_template('admin/article.html', articles=articles, categories=categories)
    return render_template('admin/add-article.html',categories=categories)

@blue2.route('/admin/updateArticle/<int:aid>/', methods=['GET', 'POST'])
def update_article(aid):
    username = session.get('username', '')
    if username == '':
        return render_template('admin/login.html')
    if request.method == 'POST':
        # 从前端表单中获取修改后的内容
        article = Article.query.get(aid)
        article.text = request.form.get('content')
        article.title = request.form.get('title')
        article.category_id = request.form.get('category')
        article.tags = request.form.get('tags')
        article.date = datetime.datetime.now()
        print(article.date)
        article.comment_count = 0  # 如果不给默认值会为None
        try:
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        articles = Article.query.all()
        categories = Category.query.all()
        return render_template('admin/article.html', articles=articles, categories=categories)
    article = Article.query.get(aid)
    categories = Category.query.all()
    return render_template('admin/update-article.html', article=article, categories=categories)

@blue2.route('/admin/deleteArticle/<int:aid>/')
def delete_article(aid):
    username = session.get("username",'')
    if username == '':
        return render_template('admin/login.html')
    article = Article.query.get(aid)
    db.session.delete(article)
    db.session.commit()
    articles = Article.query.all()
    return render_template('admin/article.html',articles=articles)


# 批量删除复选框中选中的文章
@blue2.route('/admin/deleteSelect/',methods=['GET','POST'])
def delete_select():
    username = session.get("username",'')
    if username == '':
        return render_template('admin/login.html')
    if request.method == "POST":
        check_box = request.form.getlist("checkbox[]")
        for index in check_box:
            article = Article.query.get(int(index))
            db.session.delete(article)
            db.session.commit()
        articles = Article.query.all()
        return render_template('admin/article.html',articles=articles)
        # print(check_box,type(check_box))

    # article = Article.query.get(aid)
    # db.session.delete(article)
    # db.session.commit()
    articles = Article.query.all()
    return render_template('admin/article.html',articles=articles)
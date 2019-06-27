import time

from flask import Blueprint, render_template, request, g, current_app
from flask.json import jsonify

from App.exts import cache
from App.models import *

blue = Blueprint('blog', __name__)




# 首页
@blue.route('/')
def index():
    articles = Article.query.all()
    categories = Category.query.all()
    return render_template('blog/index.html', articles=articles, categories=categories)

@blue.route('/paginate/<int:page>/')
def paginate(page):
    page = page
    per_page = 5
    p = Article.query.paginate(page, per_page, False)
    articles = p.items
    return render_template('blog/index.html', articles=articles, p=p)

# @blue.route('/getarticle/')
# def get_article():
#     articles = Article.query.all()
#     return render_template('blog/index.html', articles=articles)





# 每个分类下的文章列表
# @blue.route('/list/<int:cid>/')
# def list(cid):
#     articles = Article.query.filter_by(category_id=cid)
#     categorys = Category.query.all()
#     return render_template('blog/list.html', articles=articles, categorys=categorys)

@blue.route('/list/<int:cid>/')
def list(cid):
    articles = Article.query.filter_by(category_id=cid)
    categorys = Category.query.all()
    return render_template('blog/list.html',  articles= articles, categorys=categorys)

@blue.route('/info/')
def info():
    article = Article.query.get(1)
    categorys = Category.query.all()
    return render_template('blog/info.html', article=article, categorys=categorys)

@blue.route('/infopic/')
def infopic():
    categorys = Category.query.all()
    return render_template('blog/infopic.html', categorys=categorys)

@blue.route('/gbook/')
def gbook():
    categorys = Category.query.all()
    return render_template('blog/gbook.html', categorys=categorys)

@blue.route('/about/')
def about():
    categorys = Category.query.all()
    return render_template('blog/about.html', categorys=categorys)

@blue.route('/share/')
def share():
    categorys = Category.query.all()
    return render_template('blog/share.html', categorys=categorys)

# @blue.route('/gbook/')
# def gbook():
#     categorys = Category.query.all()
#     return render_template('blog/gbook.html', categorys=categorys)
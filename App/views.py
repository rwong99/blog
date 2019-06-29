import time

from flask import Blueprint, render_template, request, g, current_app
from flask.json import jsonify

from App.exts import cache
from App.models import *

blue = Blueprint('blog', __name__)


# 首页
@blue.route('/')
def index():
    # 分页
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 4))
    p = Article.query.paginate(page, per_page, False)
    articles = p.items
    categories = Category.query.all()
    return render_template('blog/index.html', articles=articles, categories=categories, p=p)


# 首页分页
@blue.route('/<int:page>/')
def paginate(page):
    page = page
    per_page = int(request.args.get('per_page', 4))
    p = Article.query.paginate(page, per_page, False)
    articles = p.items
    categories = Category.query.all()
    return render_template('blog/index.html', articles=articles, categories=categories, p=p)


@blue.route('/list/<int:cid>/')
def list(cid):
    articles = Article.query.filter_by(category_id=cid)
    categorys = Category.query.all()
    return render_template('blog/list.html', articles=articles, categorys=categorys)

# 每个分类下的分页
@blue.route('/list/<int:cid>/<int:page>/')
def list_paginate(cid, page):
    page = page
    per_page = int(request.args.get('per_page', 4))
    # p = Article.query.paginate(page, per_page, False)
    # articles = p.items
    articles = Article.query.filter_by(category_id=cid)
    p = articles.paginate(page, per_page, False)
    articles = p.items
    categorys = Category.query.all()
    return render_template('blog/list.html', articles=articles, categorys=categorys,p=p)


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

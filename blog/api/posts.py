from flask import jsonify, g, request, url_for, current_app
from blog.models import Post, Permission
from . import api
from .. import db
from .decorators import permission_required
from .errors import forbidden


@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', next=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next':next,
        'posts_count': pagination.total
    })


@api.route('/post/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id)}


@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if not g.current_user == post.author or \
            g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    post.body = request.args.get('body', post.body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())
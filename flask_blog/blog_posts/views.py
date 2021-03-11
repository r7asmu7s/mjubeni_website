from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.models import BlogPost
from flask_blog.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts', __name__)


@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():

    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(title=form.title.data, text=form.text.data, user_id=current_user.id)

        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created!')
        return redirect(url_for('core.blog'))

    return render_template('create_post.html', form=form, action_title='Create Post', title='mJubeni | Create Post')


@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post.title = form.title.data
        blog_post.text = form.text.data

        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Updated!')
        return redirect(url_for('core.blog', blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html', title='mJubeni | Update Post', form=form, action_title='Update Post')


@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted!')

    return redirect(url_for('core.blog'))

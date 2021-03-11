from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask.globals import session
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from flask_blog import db
from flask_blog.models import User, BlogPost
from flask_blog.users.forms import RegisterationForm, LoginForm, UpdateUserForm

users = Blueprint('users', __name__)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))


# @users.route('/_+register+_', methods=['GET', 'POST'])
# def register():
#     form = RegisterationForm()

#     if form.validate_on_submit():
#         user = User(email=form.email.data, username=form.username.data, password=form.password.data)

#         db.session.add(user)
#         db.session.commit()

#         flash('Thanks for Registeration!')

#         return redirect(url_for('users.login'))

#     return render_template('register.html', form=form)


@users.route('/_+login+_', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None:
            redirect(url_for('users.login'))

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged In Successfully!')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('users.account')

            session.pop('_flashes', None)
            return redirect(next) if next else redirect(url_for('users.account'))

        else:
            flash('Login Unsuccessful. Please check username and password.')
            return redirect(url_for('users.login'))

    return render_template('login.html', form=form, title='mJubeni | Login')


@users.route('/_+account+_', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', form=form, title='mJubeni | Dashboard')


# @users.route('/<username>')
# def user_post(username):

#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)

#     return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)

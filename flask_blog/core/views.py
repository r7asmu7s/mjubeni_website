from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from flask_blog import app
from flask_mail import Mail, Message
from flask import render_template, request, Blueprint
from flask_blog.models import BlogPost
from flask_blog.core.forms import ContactForm

core = Blueprint('core', __name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mjubeni.blog@gmail.com'
app.config['MAIL_PASSWORD'] = 'mjubenibl0gpasswordHERE!@'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.testing = False
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_DEFAULT_SENDER'] = ('mJubeni Blog', 'mjubeni.blog@gmail.com')

mail = Mail(app)


@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=1)

    return render_template('index.html', blog_posts=blog_posts, title='mJubeni')


@core.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=6)

    return render_template('blog.html', blog_posts=blog_posts, title='mJubeni | Blog')


@core.route('/about')
def about():
    return render_template('about.html', title='mJubeni | About')


@core.route('/contact', methods=['GET', 'POST'])
def contact():

    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        text = form.text.data
        email = form.email.data

        message = Message(subject=f'mJubeni Contact | {email}', recipients=['mjubeni.blog@gmail.com'], html=f'''
        <br>
        <h5>This is an automatic email,</h5>
        <br>
        <br>
        <h5>From: </h5>
        <br>        
        <h5>Name: {name}</h5>
        <br>
        <h5>Email: {email}</h5>
        <br>
        <br>
        
        <h5>Message:</h5>
        <br>
        <p>{text}</p>
        <br>
        <br>
        <br>
        End of the message.
        ''')

        mail.send(message)

        return redirect(url_for('core.contact'))

    return render_template('contact.html', title='mJubeni | Contact', form=form)

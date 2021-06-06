import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from . import app, db, bcrypt
from .models import User, Post
from .forms import RegistrationForm, LoginForm, AccountUpdateForm, BlogCreateForm


posts = [
    {
        "title": "The Imitation Game",
        "author": 'Agatha Christie',
        "read": "47,922",
        "date": "December 12, 1957",
        "content": """Pure chance led my friend Hercule Poirot, formerly chief of the Belgian force, to be 
connected with the Styles Case. His success brought him notoriety, and he decided to 
devote himself to the solving of problems in crime. Having been wounded on the Somme 
and invalided out of the Army, I finally took up my quarters with him in London. Since I 
have a first-hand knowledge of most of his cases, it has been suggested to me that I select 
some of the most interesting and place them on record. In doing so, I feel that I cannot do 
better than begin with that strange tangle which aroused such widespread public interest 
at the time. I refer to the affair at the Victory Ball. """
    },
    {
        "title": "The Hounds of Baskerville",
        "author": "Sir Arthur Conan Doyle",
        "read": "113,203",
        "date": "April 23, 1924",
        "content": """Dr James Mortimer calls on Sherlock Holmes in London for advice after his friend Sir Charles Baskerville 
        was found dead in the yew alley of his manor on Dartmoor in Devon. The death was attributed to a heart attack, but according to Mortimer, 
        Sir Charles's face retained an expression of horror, and not far from the corpse the footprints of a gigantic hound were clearly visible. 
        According to an old legend, a curse runs in the Baskerville family since the time of the English Civil War, when a Hugo Baskerville abducted and 
        caused the death of a maiden on the moor, only to be killed in turn by a huge demonic hound. Allegedly the same creature has been haunting the 
        anor ever since, causing the premature death of many Baskerville heirs. Sir Charles believed in the plague of the hound and so does Mortimer, 
        who now fears for the next in line, Sir Henry Baskerville."""
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "read": "10,127",
        "date": "July 11, 1960",
        "content": """Dr James Mortimer calls on Sherlock Holmes in London for advice after his friend Sir Charles Baskerville 
        was found dead in the yew alley of his manor on Dartmoor in Devon. The death was attributed to a heart attack, but according to Mortimer, 
        Sir Charles's face retained an expression of horror, and not far from the corpse the footprints of a gigantic hound were clearly visible. 
        According to an old legend, a curse runs in the Baskerville family since the time of the English Civil War, when a Hugo Baskerville abducted and 
        caused the death of a maiden on the moor, only to be killed in turn by a huge demonic hound. Allegedly the same creature has been haunting the 
        anor ever since, causing the premature death of many Baskerville heirs. Sir Charles believed in the plague of the hound and so does Mortimer, 
        who now fears for the next in line, Sir Henry Baskerville."""
    }
]


@app.route("/")
@app.route("/home")
def home_page():
    db_posts= Post.query.all()
    return render_template("home.html", posts=db_posts)


@app.route("/about")
def about_page():
    return render_template("about.html", title='About Page')


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login_page'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            flash('Successfully logged in!', 'success')
            return redirect(url_for('home_page'))
        else:
            flash("Email or Password is incorrect!", 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout_page():
    logout_user()
    return redirect(url_for('login_page'))


def save_picture(picture_data):
    random_hex = secrets.token_hex(8)
    _, picture_ext = os.path.splitext(picture_data.filename)
    picture_name = random_hex + picture_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics' , picture_name)
    # output_size = (125, 125)
    # image = Image.open(picture_data)
    # image.thumbnail(output_size)
    # image.save(picture_path)
    picture_data.save(picture_path)
    return picture_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account_page():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_name = save_picture(form.picture.data)
            current_user.image_file = picture_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated!', 'success')
        return redirect(url_for('account_page'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form= form)


@app.route("/blog/create", methods=['GET', 'POST'])
@login_required
def blog_create_page():
    form = BlogCreateForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Blog has been created!', 'success')
        return redirect(url_for('home_page'))
    return render_template('create_blog.html', title='New Blog', form=form, legend='New Post')


@app.route("/blog/<int:blog_id>", methods=['GET', 'POST'])
def blog_detail_page(blog_id):
    post = Post.query.get_or_404(blog_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/blog/<int:blog_id>/update", methods=['GET', 'POST'])
@login_required
def blog_update_page(blog_id):
    post = Post.query.get_or_404(blog_id)
    if post.author != current_user:
        abort(403)
    form = BlogCreateForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your blog has been updated')
        return redirect(url_for('blog_detail_page', blog_id=post.id))
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_blog.html', title='Update Post', form=form, legend='Update Post')


@app.route("/blog/<int:blog_id>/delete", methods=['POST'])
@login_required
def blog_delete_page(blog_id):
    post = Post.query.get_or_404(blog_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home_page'))


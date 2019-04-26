import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from BRF import app, db, bcrypt
from BRF.forms import RegistrationForm, LoginForm, PostForm
from BRF.models import User, Post, Styrelsen
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    posts = Post.query.all()
    return render_template('about.html', title='About', posts=posts)

@app.route("/styrelsen")
def styrelsen():
    posts = Post.query.all()
    styrelsens = Styrelsen.query.all()
    return render_template('styrelsen.html', posts=posts, styrelsens=styrelsens)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ditt konto har blivit skapat! Du har nu möjligheten att logga in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Inloggning Misslyckades. Var snäll och kolla e-mail och lösenord', 'fara')
    return render_template('login.html', title='Login', form=form)

@app.route("/news/post", methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.image_file == '2':
        form = PostForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('home'))
        return render_template('create_post.html', title='New Post',
                               form=form, legend='New Post')
    else:
        return redirect(url_for('news'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/news")
@login_required
def news():
    posts = Post.query.all()
    return render_template("news.html",title="Nyheter", posts=posts)

@app.route("/news/<int:post_id>")
def post(post_id):
    posts = Post.query.all()
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/news/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/news/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
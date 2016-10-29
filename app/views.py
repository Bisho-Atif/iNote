from app import App
from flask import render_template,session,url_for,request,flash,redirect
from app.models.models import *
import re

@App.route('/')
def index():
    name = session.get('name',None)
    return render_template('index.html',user = name)

@App.route('/hello')
def hello():
    return '<h1>Just saying Hello ;)</h1>'

@App.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            flash("The password doesn't match !!")
            return redirect('/register')

        if not re.match('[^@]+@[^@]+\.[^@]+', request.form['email']) :
            flash("The email address isn't valied !!")            
            return redirect('/register')

        user = User.query.filter_by(name = request.form['name']).first()
        if user:
            flash('The user already exists, Please try again with different user !!')
            return redirect('/register')
        else:
            new_user = User(name = request.form['name'],
                            password = request.form['password'],
                            email = request.form['email'])
            db.session.add(new_user)
            db.session.commit()
            session['name'] = request.form['name']
            user = User.query.filter_by(name = request.form['name']).first()
            session['id'] = user.id
            return redirect('/')
    return render_template('register.html')

@App.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(name = request.form['name']).first()
        if user and request.form['password'] == user.password:
            session['id'] = user.id
            session['name'] = user.name
            return redirect('/')
        else:
            flash('the name or the password is incorrect')
            return redirect('/login')
    return render_template('login.html')

@App.route('/about')
def about():
    name = session.get('name',None)
    return render_template('about.html',user = name)

@App.route('/logout')
def logout():
    session['id'] = ''
    session['name'] = ''
    return redirect('/')

@App.route('/change_password', methods=['GET', 'POST'])
def change_passwrod():
    name = session.get('name',None)
    if request.method == 'POST':
        user = User.query.filter_by(name = session['name']).first()
        print user.password
        if request.form['old_password'] != user.password:
            flash('The old password is incorrect')
            return redirect('/change_password')
        if request.form['new_password'] != request.form['confirm_password']:
            flash("The password doesn't match")
            return redirect('/change_password')
        user.password = request.form['new_password']
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('change_password.html',user = name)

@App.route('/notes')
def notes():
    name = session.get('name',None)
    notes = User.query.filter_by(name= session['name']).first().notes    
    return render_template('notes.html', user=name, notes=notes)

@App.route('/add_note', methods=['GET','POST'])
def add_note():
    name = session.get('name',None)
    if request.method == 'POST':
        new_note = Note(title = request.form['title'],
                        content= request.form['content'],
                        user_id= session['id'] )
        db.session.add(new_note)
        db.session.commit()
        return redirect('/notes')
    return render_template('add_note.html', user=name)

@App.route('/delete_note/<int:id>')
def delete_note(id):
    note = Note.query.filter_by(id = id)[0]
    if note.user_id != session['id']:
        flash("You don't have the permission to do this")
        return redirect('/notes')
    db.session.delete(note)
    db.session.commit()
    return redirect('/notes')

@App.route('/edit_note/<int:id>', methods=['POST','GET'])
def edit_note(id):
    name = session.get('name',None)
    note = Note.query.filter_by(id = id)[0]
    if note.user_id != session['id']:
        flash("You don't have the permission to do this")
        return redirect('/notes')
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.add(note)
        db.session.commit()
    else:
        return render_template('/edit_note.html',note=note, user= name )
    return redirect('/notes')
















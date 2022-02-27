from tkinter import N
from turtle import title
from flask import render_template, redirect, request, url_for
from premier import app, db
from premier.models import Team

@app.route('/')
def index():
    return render_template('index.html', title='Home Page')

@app.route('/teams')
def teams():
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM team')
    rs = cursor.fetchall()
    cursor.close()
    # print(teams)
    teams = []
    for t in rs:
        team = Team(id=t[0], name=t[1], city=t[2], image=t[3])
        teams.append(team)

    return render_template('teams.html', title='All Teams', teams=teams)

@app.route('/team/add', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form['city']

        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO team(name, city) VALUES(%s, %s)', (name, city))
        cursor.connection.commit()

        cursor.close()
        return redirect(url_for('teams'))

    return render_template('add_team.html', title='Add New Team')

@app.route('/team/update/<int:id>', methods=['GET', 'POST'])
def update_team(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM team WHERE id = %s', (id,))
    rs = cursor.fetchone()
    cursor.close()
    team = Team(id=rs[0], name=rs[1], city=rs[2], image=rs[3])

    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form['city']

        cursor = db.connection.cursor()
        cursor.execute('UPDATE team SET name=%s, city=%s WHERE id = %s', (name, city, id))
        cursor.connection.commit()

        cursor.close()
        return redirect(url_for('teams'))
        
    return render_template('update_team.html', title='Update Team', team=team)
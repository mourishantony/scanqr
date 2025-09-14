from flask import Response
import csv
from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profiles.db'
db = SQLAlchemy(app)

@app.route('/download_csv')
def download_csv():
    profiles = Profile.query.all()
    def generate():
        data = [['Name', 'Profile Link']]
        for p in profiles:
            data.append([p.name, p.link])
        output = []
        for row in data:
            output.append(','.join('"{}"'.format(str(cell).replace('"', '""')) for cell in row))
        return '\r\n'.join(output)
    csv_data = generate()
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=profiles.csv"}
    )

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    link = db.Column(db.String(300), nullable=False)

@app.route('/')
def index():
    return render_template('scan.html')

@app.route('/profiles')
def profiles():
    all_profiles = Profile.query.all()
    return render_template('profiles.html', profiles=all_profiles)

@app.route('/add_profile', methods=['POST'])
def add_profile():
    data = request.json
    name = data.get('name')
    link = data.get('link')
    if name and link:
        new_profile = Profile(name=name, link=link)
        db.session.add(new_profile)
        db.session.commit()
        return {'status': 'success'}, 201
    return {'status': 'error'}, 400

@app.route('/delete_all_profiles', methods=['POST','DELETE'])
def delete_all_profiles():
    try:
        num_deleted = db.session.query(Profile).delete(synchronize_session=False)
        db.session.commit()
        return jsonify(status='success', deleted=num_deleted)
    except Exception as e:
        db.session.rollback()
        return jsonify(status='error', error=str(e)), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

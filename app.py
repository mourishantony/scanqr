from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profiles.db'
db = SQLAlchemy(app)
@app.route('/download_db')
def download_db():
    db_path = os.environ.get('DATABASE_URL', None)
    if db_path and db_path.startswith('sqlite:///'):
        db_file = db_path.replace('sqlite:///', '')
    else:
        db_file = 'profiles.db'
    if os.path.exists(db_file):
        return send_file(db_file, as_attachment=True)
    return 'Database file not found.', 404

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from Backend.main_crawler import search_all
from Backend.database import db
from Backend.models_db import User, Favorite
from config import SECRET_KEY
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///announcefinder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# ------------------- Pages ------------------ #
@app.route('/')
def index():
    return send_from_directory('Frontend', 'MainPage.html')

@app.route('/login')
def login_page():
    return send_from_directory('Frontend', 'LoginPage.html')

@app.route('/favorites')
def favorites_page():
    return send_from_directory('Frontend', 'AccountPage.html')

@app.route('/Style.css')
def styles():
    return send_from_directory('Frontend', 'Style.css')

#------------------- Search ------------------ #
@app.route('/search')
def search():
    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 10))
    if not query:
        return jsonify([])
    results = search_all(query, limit)
    return jsonify([result.__dict__ for result in results])


#------------------- Authentication ------------------ #
def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email address'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return jsonify({'success': True})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    login_user(user)
    return jsonify({'success': True})

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'success': True})

@app.route('/me')
def me():
    if current_user.is_authenticated:
        return jsonify({'logged_in': True, 'email': current_user.email})
    return jsonify({'logged_in': False})

#------------------- Favorites ------------------ #
@app.route('/favorites/add', methods=['POST'])
def add_favorite():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    if Favorite.query.filter_by(user_id=current_user.id, 
                                listing_id=data['listing_id']).first():
        return jsonify({'error': 'Already in favorites'}), 400
    
    fav = Favorite(
        user_id = current_user.id,
        listing_id = data['listing_id'],
        title = data['title'],
        platform = data['platform'],
        price = data['price'],
        url = data['url'],
        image = data['image']
    )
    db.session.add(fav)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/favorites/remove', methods=['POST'])
def remove_favorite():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not logged in'}), 401
    data = request.get_json()
    fav  = Favorite.query.filter_by(user_id=current_user.id, listing_id=data['listing_id']).first()
    if not fav:
        return jsonify({'error': 'Not in favorites'}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/favorites/get')
def get_favorites():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not logged in'}), 401
    favs = Favorite.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'listing_id': f.listing_id,
        'title':      f.title,
        'platform':   f.platform,
        'price':      f.price,
        'url':        f.url,
        'image':      f.image
    } for f in favs])

if __name__ == '__main__':
    app.run(debug=True)
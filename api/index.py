"""
Flask Web Application for Instagram Follower Analyzer
Vercel Serverless Functions Compatible
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from functools import wraps
import json
from datetime import datetime
from instagram_api import InstagramClient
from follower_analyzer import FollowerAnalyzer
from config import Config

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
CORS(app)

# Configure upload folder
Config.ensure_cache_dir()


def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    """Login endpoint"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Try to login
        client = InstagramClient()
        if client.login(username, password):
            session['username'] = username
            session['user_id'] = client.user_id
            
            return jsonify({
                'success': True,
                'message': f'Successfully logged in as {username}',
                'username': username
            })
        else:
            return jsonify({'error': 'Login failed'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Logout endpoint"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@app.route('/api/user', methods=['GET'])
@login_required
def api_user():
    """Get current user info"""
    try:
        username = session.get('username')
        client = InstagramClient()
        client.login()
        
        user_info = client.get_user_info()
        return jsonify(user_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/fetch', methods=['POST'])
@login_required
def api_fetch():
    """Fetch followers and following data"""
    try:
        username = session.get('username')
        client = InstagramClient()
        client.login()
        
        followers = client.get_followers()
        following = client.get_following()
        
        # Save data
        client.save_data(followers, following)
        
        return jsonify({
            'success': True,
            'message': 'Data fetched successfully',
            'followers_count': len(followers),
            'following_count': len(following)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis', methods=['GET'])
@login_required
def api_analysis():
    """Get analysis results"""
    try:
        cache_dir = Config.CACHE_DIR
        
        # Find latest cache files
        followers_files = [f for f in os.listdir(cache_dir) if f.endswith('_followers_*.json')]
        following_files = [f for f in os.listdir(cache_dir) if f.endswith('_following_*.json')]
        
        if not followers_files or not following_files:
            return jsonify({'error': 'No cached data found'}), 404
        
        # Load latest files
        followers_file = os.path.join(cache_dir, sorted(followers_files)[-1])
        following_file = os.path.join(cache_dir, sorted(following_files)[-1])
        
        with open(followers_file, 'r', encoding='utf-8') as f:
            followers = json.load(f)
        
        with open(following_file, 'r', encoding='utf-8') as f:
            following = json.load(f)
        
        # Convert string keys back to integers
        followers = {int(uid): info for uid, info in followers.items()}
        following = {int(uid): info for uid, info in following.items()}
        
        # Create analyzer
        analyzer = FollowerAnalyzer(followers, following)
        stats = analyzer.get_statistics()
        summary = analyzer.export_comparison_summary()
        
        # Get specific lists
        one_way_followers = analyzer.get_one_way_followers()
        not_following_back = analyzer.get_one_way_following()
        mutuals = analyzer.get_mutual_followers()
        
        return jsonify({
            'statistics': {
                'total_followers': stats.total_followers,
                'total_following': stats.total_following,
                'mutual_follows': stats.mutual_follows,
                'one_way_followers': stats.one_way_followers,
                'one_way_following': stats.one_way_following,
                'engagement_ratio': stats.engagement_ratio,
                'follow_back_ratio': stats.follow_back_ratio,
            },
            'summary': summary,
            'one_way_followers_count': len(one_way_followers),
            'not_following_back_count': len(not_following_back),
            'mutuals_count': len(mutuals),
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/unfollowers', methods=['GET'])
@login_required
def api_unfollowers():
    """Get one-way followers (unfollowers)"""
    try:
        limit = request.args.get('limit', 20, type=int)
        filter_keyword = request.args.get('filter', '', type=str)
        
        cache_dir = Config.CACHE_DIR
        followers_files = [f for f in os.listdir(cache_dir) if f.endswith('_followers_*.json')]
        following_files = [f for f in os.listdir(cache_dir) if f.endswith('_following_*.json')]
        
        if not followers_files or not following_files:
            return jsonify({'error': 'No cached data found'}), 404
        
        followers_file = os.path.join(cache_dir, sorted(followers_files)[-1])
        following_file = os.path.join(cache_dir, sorted(following_files)[-1])
        
        with open(followers_file, 'r', encoding='utf-8') as f:
            followers = json.load(f)
        
        with open(following_file, 'r', encoding='utf-8') as f:
            following = json.load(f)
        
        followers = {int(uid): info for uid, info in followers.items()}
        following = {int(uid): info for uid, info in following.items()}
        
        analyzer = FollowerAnalyzer(followers, following)
        one_way = analyzer.get_one_way_followers()
        
        if filter_keyword:
            one_way = analyzer.filter_by_keyword(one_way, filter_keyword)
        
        # Convert to list and limit
        results = [
            {
                'id': uid,
                'username': info['username'],
                'full_name': info.get('full_name', 'N/A'),
                'is_verified': info.get('is_verified', False),
                'is_private': info.get('is_private', False)
            }
            for uid, info in list(one_way.items())[:limit]
        ]
        
        return jsonify({
            'total': len(one_way),
            'count': len(results),
            'data': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/not-following-back', methods=['GET'])
@login_required
def api_not_following_back():
    """Get people you follow but who don't follow back"""
    try:
        limit = request.args.get('limit', 20, type=int)
        filter_keyword = request.args.get('filter', '', type=str)
        
        cache_dir = Config.CACHE_DIR
        followers_files = [f for f in os.listdir(cache_dir) if f.endswith('_followers_*.json')]
        following_files = [f for f in os.listdir(cache_dir) if f.endswith('_following_*.json')]
        
        if not followers_files or not following_files:
            return jsonify({'error': 'No cached data found'}), 404
        
        followers_file = os.path.join(cache_dir, sorted(followers_files)[-1])
        following_file = os.path.join(cache_dir, sorted(following_files)[-1])
        
        with open(followers_file, 'r', encoding='utf-8') as f:
            followers = json.load(f)
        
        with open(following_file, 'r', encoding='utf-8') as f:
            following = json.load(f)
        
        followers = {int(uid): info for uid, info in followers.items()}
        following = {int(uid): info for uid, info in following.items()}
        
        analyzer = FollowerAnalyzer(followers, following)
        one_way = analyzer.get_one_way_following()
        
        if filter_keyword:
            one_way = analyzer.filter_by_keyword(one_way, filter_keyword)
        
        results = [
            {
                'id': uid,
                'username': info['username'],
                'full_name': info.get('full_name', 'N/A'),
                'is_verified': info.get('is_verified', False),
                'is_private': info.get('is_private', False)
            }
            for uid, info in list(one_way.items())[:limit]
        ]
        
        return jsonify({
            'total': len(one_way),
            'count': len(results),
            'data': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mutual', methods=['GET'])
@login_required
def api_mutual():
    """Get mutual followers"""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        cache_dir = Config.CACHE_DIR
        followers_files = [f for f in os.listdir(cache_dir) if f.endswith('_followers_*.json')]
        following_files = [f for f in os.listdir(cache_dir) if f.endswith('_following_*.json')]
        
        if not followers_files or not following_files:
            return jsonify({'error': 'No cached data found'}), 404
        
        followers_file = os.path.join(cache_dir, sorted(followers_files)[-1])
        following_file = os.path.join(cache_dir, sorted(following_files)[-1])
        
        with open(followers_file, 'r', encoding='utf-8') as f:
            followers = json.load(f)
        
        with open(following_file, 'r', encoding='utf-8') as f:
            following = json.load(f)
        
        followers = {int(uid): info for uid, info in followers.items()}
        following = {int(uid): info for uid, info in following.items()}
        
        analyzer = FollowerAnalyzer(followers, following)
        mutuals = analyzer.get_mutual_followers()
        
        results = [
            {
                'id': uid,
                'username': info[0]['username'],
                'full_name': info[0].get('full_name', 'N/A'),
                'is_verified': info[0].get('is_verified', False),
            }
            for uid, info in list(mutuals.items())[:limit]
        ]
        
        return jsonify({
            'total': len(mutuals),
            'count': len(results),
            'data': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'OK', 'timestamp': datetime.now().isoformat()})


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500

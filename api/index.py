"""
Flask Web Application for Instagram Follower Analyzer
Vercel Serverless Functions Compatible
"""
import json
import os
import sys
from datetime import datetime
from functools import wraps
from glob import glob

from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

InstagramClient = None
FollowerAnalyzer = None
INSTAGRAM_IMPORT_ERROR = None
ANALYZER_IMPORT_ERROR = None

try:
    from instagram_api import InstagramClient
except Exception as exc:
    INSTAGRAM_IMPORT_ERROR = exc

try:
    from follower_analyzer import FollowerAnalyzer
except Exception as exc:
    ANALYZER_IMPORT_ERROR = exc

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'vercel-secret-key')
CORS(app)
Config.ensure_cache_dir()

if INSTAGRAM_IMPORT_ERROR:
    print(
        "Instagram client import failed: "
        f"{type(INSTAGRAM_IMPORT_ERROR).__name__}: {INSTAGRAM_IMPORT_ERROR}"
    )

if ANALYZER_IMPORT_ERROR:
    print(
        "Follower analyzer import failed: "
        f"{type(ANALYZER_IMPORT_ERROR).__name__}: {ANALYZER_IMPORT_ERROR}"
    )


def instagram_client_ready():
    """Return True when the Instagram client imported successfully."""
    return InstagramClient is not None


def analyzer_ready():
    """Return True when the follower analyzer imported successfully."""
    return FollowerAnalyzer is not None


def dependency_error_response(name, error):
    """Return a stable JSON response when an optional dependency is unavailable."""
    return jsonify({
        'error': f'{name} is not available in this deployment',
        'details': str(error) if error else None,
    }), 503


def load_cached_data():
    """Load the latest follower/following cache files from disk."""
    followers_files = sorted(glob(os.path.join(Config.CACHE_DIR, '*_followers_*.json')))
    following_files = sorted(glob(os.path.join(Config.CACHE_DIR, '*_following_*.json')))

    if not followers_files or not following_files:
        raise FileNotFoundError('No cached data found')

    with open(followers_files[-1], 'r', encoding='utf-8') as f:
        followers = json.load(f)

    with open(following_files[-1], 'r', encoding='utf-8') as f:
        following = json.load(f)

    return (
        {int(uid): info for uid, info in followers.items()},
        {int(uid): info for uid, info in following.items()},
    )


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
    try:
        return render_template('index.html')
    except Exception:
        return jsonify({
            'app': 'Instagram Follower Analyzer',
            'version': '1.0.0',
            'status': 'API is running',
            'instagram_client_ready': instagram_client_ready(),
            'analyzer_ready': analyzer_ready(),
            'cache_dir': Config.CACHE_DIR,
            'endpoints': {
                '/api/health': 'Health check',
                '/api/login': 'POST - Login',
                '/api/logout': 'POST - Logout',
                '/api/fetch': 'POST - Fetch data',
                '/api/analysis': 'GET - Get analysis',
                '/api/unfollowers': 'GET - Get unfollowers',
                '/api/not-following-back': 'GET - Get not following back',
                '/api/mutual': 'GET - Get mutual followers',
            },
        })


@app.route('/api/login', methods=['POST'])
def api_login():
    """Login endpoint"""
    if not instagram_client_ready():
        return dependency_error_response('Instagram client', INSTAGRAM_IMPORT_ERROR)

    try:
        data = request.json or {}
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400

        client = InstagramClient()
        if client.login(username, password):
            session['username'] = username
            session['user_id'] = client.user_id

            return jsonify({
                'success': True,
                'message': f'Successfully logged in as {username}',
                'username': username,
            })

        return jsonify({'error': 'Login failed'}), 401
    except Exception as e:
        return jsonify({'error': f'Login error: {str(e)}'}), 500


@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Logout endpoint"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@app.route('/api/user', methods=['GET'])
@login_required
def api_user():
    """Get current user info"""
    if not instagram_client_ready():
        return dependency_error_response('Instagram client', INSTAGRAM_IMPORT_ERROR)

    try:
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
    if not instagram_client_ready():
        return dependency_error_response('Instagram client', INSTAGRAM_IMPORT_ERROR)

    try:
        client = InstagramClient()
        client.login()

        followers = client.get_followers()
        following = client.get_following()

        client.save_data(followers, following)

        return jsonify({
            'success': True,
            'message': 'Data fetched successfully',
            'followers_count': len(followers),
            'following_count': len(following),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis', methods=['GET'])
@login_required
def api_analysis():
    """Get analysis results"""
    if not analyzer_ready():
        return dependency_error_response('Follower analyzer', ANALYZER_IMPORT_ERROR)

    try:
        followers, following = load_cached_data()

        analyzer = FollowerAnalyzer(followers, following)
        stats = analyzer.get_statistics()
        summary = analyzer.export_comparison_summary()

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
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/unfollowers', methods=['GET'])
@login_required
def api_unfollowers():
    """Get one-way followers (unfollowers)"""
    if not analyzer_ready():
        return dependency_error_response('Follower analyzer', ANALYZER_IMPORT_ERROR)

    try:
        limit = request.args.get('limit', 20, type=int)
        filter_keyword = request.args.get('filter', '', type=str)
        followers, following = load_cached_data()

        analyzer = FollowerAnalyzer(followers, following)
        one_way = analyzer.get_one_way_followers()

        if filter_keyword:
            one_way = analyzer.filter_by_keyword(one_way, filter_keyword)

        results = [
            {
                'id': uid,
                'username': info['username'],
                'full_name': info.get('full_name', 'N/A'),
                'is_verified': info.get('is_verified', False),
                'is_private': info.get('is_private', False),
            }
            for uid, info in list(one_way.items())[:limit]
        ]

        return jsonify({
            'total': len(one_way),
            'count': len(results),
            'data': results,
        })
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/not-following-back', methods=['GET'])
@login_required
def api_not_following_back():
    """Get people you follow but who don't follow back"""
    if not analyzer_ready():
        return dependency_error_response('Follower analyzer', ANALYZER_IMPORT_ERROR)

    try:
        limit = request.args.get('limit', 20, type=int)
        filter_keyword = request.args.get('filter', '', type=str)
        followers, following = load_cached_data()

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
                'is_private': info.get('is_private', False),
            }
            for uid, info in list(one_way.items())[:limit]
        ]

        return jsonify({
            'total': len(one_way),
            'count': len(results),
            'data': results,
        })
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mutual', methods=['GET'])
@login_required
def api_mutual():
    """Get mutual followers"""
    if not analyzer_ready():
        return dependency_error_response('Follower analyzer', ANALYZER_IMPORT_ERROR)

    try:
        limit = request.args.get('limit', 20, type=int)
        followers, following = load_cached_data()

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
            'data': results,
        })
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.now().isoformat(),
        'instagram_client_ready': instagram_client_ready(),
        'instagram_import_error': str(INSTAGRAM_IMPORT_ERROR) if INSTAGRAM_IMPORT_ERROR else None,
        'analyzer_ready': analyzer_ready(),
        'analyzer_import_error': str(ANALYZER_IMPORT_ERROR) if ANALYZER_IMPORT_ERROR else None,
        'cache_dir': Config.CACHE_DIR,
    })


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500

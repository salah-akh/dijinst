"""
Configuration management for Instagram Follower Analyzer
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Instagram API configuration
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
    INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
    
    # API endpoints
    INSTAGRAM_API_BASE_URL = "https://graph.instagram.com/v18.0"
    
    # API credentials (for official API)
    API_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    
    # Cache configuration
    CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True').lower() == 'true'
    
    # Output configuration
    OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'table')  # table, json, csv
    
    @staticmethod
    def ensure_cache_dir():
        """Create cache directory if it doesn't exist"""
        if not os.path.exists(Config.CACHE_DIR):
            os.makedirs(Config.CACHE_DIR)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    CACHE_ENABLED = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    CACHE_ENABLED = True


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig()
    return DevelopmentConfig()

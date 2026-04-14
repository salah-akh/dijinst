"""
Instagram Follower Analyzer Package
"""

__version__ = "1.0.0"
__author__ = "Instagram Analyzer"
__description__ = "Analyze Instagram follower relationships"

from .instagram_api import InstagramClient
from .follower_analyzer import FollowerAnalyzer, FollowerStats

__all__ = [
    'InstagramClient',
    'FollowerAnalyzer',
    'FollowerStats'
]

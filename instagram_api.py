"""
Instagram API Client for fetching followers and following lists
"""
import json
import os
from typing import List, Dict, Set
from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from config import Config


class InstagramClient:
    """Handles Instagram API authentication and data fetching"""
    
    def __init__(self):
        self.client = Client()
        self.session_file = os.path.join(Config.CACHE_DIR, 'session.json')
        self.user_id = None
        self.username = None
        
    def login(self, username: str = None, password: str = None) -> bool:
        """
        Authenticate with Instagram
        
        Args:
            username: Instagram username (uses env if not provided)
            password: Instagram password (uses env if not provided)
            
        Returns:
            bool: True if login successful
        """
        username = username or Config.INSTAGRAM_USERNAME
        password = password or Config.INSTAGRAM_PASSWORD
        
        if not username or not password:
            raise ValueError("Instagram credentials not provided. Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env file")
        
        try:
            # Try to load saved session
            if os.path.exists(self.session_file):
                self.client.load_settings(self.session_file)
                try:
                    self.client.get_me()
                    print(f"✓ Saved session loaded for {username}")
                    self.username = username
                    return True
                except LoginRequired:
                    print("✗ Saved session expired, logging in again...")
            
            # Login with credentials
            self.client.login(username, password)
            self.client.dump_settings(self.session_file)
            
            self.user_id = self.client.user_id
            self.username = username
            print(f"✓ Successfully logged in as {username}")
            return True
            
        except Exception as e:
            print(f"✗ Login failed: {str(e)}")
            raise
    
    def get_followers(self, user_id: int = None) -> Dict[int, Dict]:
        """
        Get follower list
        
        Args:
            user_id: Instagram user ID (uses authenticated user if not provided)
            
        Returns:
            Dict: Follower data {user_id: user_info}
        """
        if not user_id:
            user_id = self.client.user_id
        
        print(f"Fetching followers for user {user_id}...")
        followers = {}
        
        try:
            follower_list = self.client.user_followers(user_id)
            
            for follower in follower_list:
                followers[follower.pk] = {
                    'username': follower.username,
                    'full_name': follower.full_name,
                    'is_private': follower.is_private,
                    'is_verified': follower.is_verified
                }
            
            print(f"✓ Retrieved {len(followers)} followers")
            return followers
            
        except Exception as e:
            print(f"✗ Error fetching followers: {str(e)}")
            raise
    
    def get_following(self, user_id: int = None) -> Dict[int, Dict]:
        """
        Get following list
        
        Args:
            user_id: Instagram user ID (uses authenticated user if not provided)
            
        Returns:
            Dict: Following data {user_id: user_info}
        """
        if not user_id:
            user_id = self.client.user_id
        
        print(f"Fetching following list for user {user_id}...")
        following = {}
        
        try:
            following_list = self.client.user_following(user_id)
            
            for followee in following_list:
                following[followee.pk] = {
                    'username': followee.username,
                    'full_name': followee.full_name,
                    'is_private': followee.is_private,
                    'is_verified': followee.is_verified
                }
            
            print(f"✓ Retrieved {len(following)} accounts being followed")
            return following
            
        except Exception as e:
            print(f"✗ Error fetching following list: {str(e)}")
            raise
    
    def get_user_info(self, user_id: int = None) -> Dict:
        """Get user information"""
        if not user_id:
            user_id = self.client.user_id
        
        try:
            user = self.client.user_info(user_id)
            return {
                'id': user.pk,
                'username': user.username,
                'full_name': user.full_name,
                'biography': user.biography,
                'follower_count': user.follower_count,
                'following_count': user.following_count,
                'is_verified': user.is_verified,
                'is_private': user.is_private
            }
        except Exception as e:
            print(f"✗ Error fetching user info: {str(e)}")
            raise
    
    def save_data(self, followers: Dict, following: Dict, filename_prefix: str = None) -> str:
        """Save follower and following data to JSON files"""
        if not filename_prefix:
            filename_prefix = self.username or 'instagram_data'
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        followers_file = os.path.join(Config.CACHE_DIR, f'{filename_prefix}_followers_{timestamp}.json')
        following_file = os.path.join(Config.CACHE_DIR, f'{filename_prefix}_following_{timestamp}.json')
        
        with open(followers_file, 'w', encoding='utf-8') as f:
            json.dump(followers, f, ensure_ascii=False, indent=2)
        
        with open(following_file, 'w', encoding='utf-8') as f:
            json.dump(following, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Data saved to cache directory")
        return Config.CACHE_DIR

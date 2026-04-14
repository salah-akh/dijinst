"""
Follower Analysis Module - Compare followers and following lists
"""
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class FollowerStats:
    """Statistics about follower relationships"""
    total_followers: int
    total_following: int
    mutual_follows: int
    one_way_followers: int  # people who follow you but you don't follow back
    one_way_following: int  # people you follow but who don't follow back
    
    @property
    def engagement_ratio(self) -> float:
        """Calculate engagement ratio (mutual follows / total followers)"""
        if self.total_followers == 0:
            return 0
        return round((self.mutual_follows / self.total_followers) * 100, 2)
    
    @property
    def follow_back_ratio(self) -> float:
        """Calculate follow-back ratio (mutual follows / total following)"""
        if self.total_following == 0:
            return 0
        return round((self.mutual_follows / self.total_following) * 100, 2)


class FollowerAnalyzer:
    """Analyze and compare follower and following lists"""
    
    def __init__(self, followers: Dict[int, Dict], following: Dict[int, Dict]):
        """
        Initialize analyzer with follower and following data
        
        Args:
            followers: Dict of follower data {user_id: user_info}
            following: Dict of following data {user_id: user_info}
        """
        self.followers = followers
        self.following = following
        self.follower_ids: Set[int] = set(followers.keys())
        self.following_ids: Set[int] = set(following.keys())
    
    def get_mutual_followers(self) -> Dict[int, Tuple[Dict, Dict]]:
        """
        Get people who follow you and you follow back
        
        Returns:
            Dict: {user_id: (follower_info, following_info)}
        """
        mutual_ids = self.follower_ids & self.following_ids
        return {
            uid: (self.followers[uid], self.following[uid])
            for uid in mutual_ids
        }
    
    def get_one_way_followers(self) -> Dict[int, Dict]:
        """
        Get people who follow you but you don't follow back
        
        Returns:
            Dict: {user_id: user_info}
        """
        one_way_ids = self.follower_ids - self.following_ids
        return {uid: self.followers[uid] for uid in one_way_ids}
    
    def get_one_way_following(self) -> Dict[int, Dict]:
        """
        Get people you follow but who don't follow back
        
        Returns:
            Dict: {user_id: user_info}
        """
        one_way_ids = self.following_ids - self.follower_ids
        return {uid: self.following[uid] for uid in one_way_ids}
    
    def get_statistics(self) -> FollowerStats:
        """
        Calculate statistics about follower relationships
        
        Returns:
            FollowerStats: Statistics object
        """
        mutual = self.get_mutual_followers()
        one_way_followers = self.get_one_way_followers()
        one_way_following = self.get_one_way_following()
        
        return FollowerStats(
            total_followers=len(self.followers),
            total_following=len(self.following),
            mutual_follows=len(mutual),
            one_way_followers=len(one_way_followers),
            one_way_following=len(one_way_following)
        )
    
    def get_verified_followers(self) -> Dict[int, Dict]:
        """Get verified followers"""
        return {
            uid: info for uid, info in self.followers.items()
            if info.get('is_verified', False)
        }
    
    def get_private_followers(self) -> Dict[int, Dict]:
        """Get private account followers"""
        return {
            uid: info for uid, info in self.followers.items()
            if info.get('is_private', False)
        }
    
    def get_inactive_followers(self) -> Dict[int, Dict]:
        """Get followers who might be inactive (no full name and private)"""
        return {
            uid: info for uid, info in self.followers.items()
            if not info.get('full_name') and info.get('is_private', False)
        }
    
    def filter_by_keyword(self, data: Dict[int, Dict], keyword: str) -> Dict[int, Dict]:
        """
        Filter user data by keyword in username or full name
        
        Args:
            data: User data dictionary
            keyword: Search keyword
            
        Returns:
            Dict: Filtered results
        """
        keyword = keyword.lower()
        return {
            uid: info for uid, info in data.items()
            if keyword in info.get('username', '').lower() or
               keyword in info.get('full_name', '').lower()
        }
    
    def export_comparison_summary(self) -> Dict:
        """Export complete comparison summary"""
        stats = self.get_statistics()
        
        return {
            'statistics': {
                'total_followers': stats.total_followers,
                'total_following': stats.total_following,
                'mutual_follows': stats.mutual_follows,
                'one_way_followers': stats.one_way_followers,
                'one_way_following': stats.one_way_following,
                'engagement_ratio': f"{stats.engagement_ratio}%",
                'follow_back_ratio': f"{stats.follow_back_ratio}%"
            },
            'verified_followers': len(self.get_verified_followers()),
            'private_followers': len(self.get_private_followers()),
            'inactive_followers': len(self.get_inactive_followers())
        }

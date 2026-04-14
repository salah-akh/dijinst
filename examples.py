#!/usr/bin/env python3
"""
Quick Start Example - Instagram Follower Analyzer
Shows how to use the library programmatically
"""

from instagram_api import InstagramClient
from follower_analyzer import FollowerAnalyzer
from utils import DataExporter
import os


def example_basic_usage():
    """Basic usage example"""
    
    # 1. Create client and login
    client = InstagramClient()
    client.login()  # Uses .env credentials
    
    # 2. Fetch data
    followers = client.get_followers()
    following = client.get_following()
    
    # 3. Create analyzer
    analyzer = FollowerAnalyzer(followers, following)
    
    # 4. Get analysis results
    stats = analyzer.get_statistics()
    print(f"Total followers: {stats.total_followers}")
    print(f"Mutual follows: {stats.mutual_follows}")
    print(f"Engagement ratio: {stats.engagement_ratio}%")
    
    # 5. Get specific lists
    one_way = analyzer.get_one_way_followers()
    mutuals = analyzer.get_mutual_followers()
    
    print(f"One-way followers: {len(one_way)}")
    print(f"Mutual followers: {len(mutuals)}")


def example_filtering():
    """Example with filtering"""
    
    client = InstagramClient()
    client.login()
    
    followers = client.get_followers()
    analyzer = FollowerAnalyzer(followers, {})
    
    # Filter by keyword
    john_followers = analyzer.filter_by_keyword(followers, 'john')
    print(f"Found {len(john_followers)} followers with 'john' in name/username")
    
    # Get verified followers
    verified = analyzer.get_verified_followers()
    print(f"Verified followers: {len(verified)}")
    
    # Get private accounts
    private = analyzer.get_private_followers()
    print(f"Private followers: {len(private)}")


def example_export():
    """Example with data export"""
    
    client = InstagramClient()
    client.login()
    
    followers = client.get_followers()
    following = client.get_following()
    analyzer = FollowerAnalyzer(followers, following)
    
    exporter = DataExporter()
    
    # Export to JSON
    one_way = analyzer.get_one_way_followers()
    json_path = exporter.to_json(
        {str(uid): info for uid, info in one_way.items()},
        'exports/one_way_followers.json'
    )
    print(f"Exported to: {json_path}")
    
    # Export to CSV
    csv_path = exporter.to_csv(
        one_way,
        'exports/one_way_followers.csv',
        ['username', 'full_name', 'is_verified', 'is_private']
    )
    print(f"Exported to: {csv_path}")
    
    # Export to HTML
    html_path = exporter.to_html_report(analyzer, 'exports/report.html')
    print(f"Exported to: {html_path}")


def example_batch_analysis():
    """Example batch analysis of multiple metrics"""
    
    client = InstagramClient()
    client.login()
    
    # Get data
    followers = client.get_followers()
    following = client.get_following()
    user_info = client.get_user_info()
    
    # Create analyzer
    analyzer = FollowerAnalyzer(followers, following)
    
    # Get complete analysis
    analysis = {
        'user': user_info,
        'statistics': analyzer.export_comparison_summary(),
        'one_way_followers': list(analyzer.get_one_way_followers().keys())[:10],
        'one_way_following': list(analyzer.get_one_way_following().keys())[:10],
    }
    
    # Export everything
    exporter = DataExporter()
    exporter.to_json(analysis, 'exports/complete_analysis.json')
    print("Complete analysis exported")


if __name__ == '__main__':
    # Uncomment the example you want to run:
    
    # example_basic_usage()
    # example_filtering()
    # example_export()
    # example_batch_analysis()
    
    print("Edit this file and uncomment the example you want to run!")

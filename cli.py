"""
Instagram Follower Analyzer CLI
Command-line interface for analyzing follower relationships
"""
import click
import os
import json
from tabulate import tabulate
from config import Config
from instagram_api import InstagramClient
from follower_analyzer import FollowerAnalyzer


# Ensure cache directory exists
Config.ensure_cache_dir()


@click.group()
def cli():
    """Instagram Follower Analyzer - Analyze your follower relationships"""
    pass


@cli.command()
@click.option('--username', prompt='Instagram username', help='Instagram username')
@click.option('--password', prompt='Instagram password', hide_input=True, help='Instagram password')
def login(username: str, password: str):
    """Login to Instagram and save session"""
    try:
        client = InstagramClient()
        if client.login(username, password):
            click.echo(click.style("✓ Login successful!", fg='green'))
    except Exception as e:
        click.echo(click.style(f"✗ Login failed: {str(e)}", fg='red'))


@cli.command()
def fetch():
    """Fetch followers and following lists"""
    try:
        client = InstagramClient()
        
        # Try to load saved session
        if not os.path.exists(os.path.join(Config.CACHE_DIR, 'session.json')):
            click.echo(click.style("✗ No saved session found. Please login first:", fg='red'))
            click.echo("  instagram-analyzer login")
            return
        
        # Load session
        client.client.load_settings(os.path.join(Config.CACHE_DIR, 'session.json'))
        
        click.echo(click.style("📊 Fetching Instagram data...", fg='cyan'))
        
        # Get user info
        user_info = client.get_user_info()
        click.echo(f"\n👤 User: {user_info['username']}")
        click.echo(f"   Followers: {user_info['follower_count']}")
        click.echo(f"   Following: {user_info['following_count']}\n")
        
        # Get followers and following
        followers = client.get_followers()
        following = client.get_following()
        
        # Save data
        client.save_data(followers, following)
        
        click.echo(click.style("\n✓ Data fetched and cached successfully!", fg='green'))
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg='red'))


@cli.command()
@click.option('--sort', type=click.Choice(['followers', 'name', 'verified']), 
              default='followers', help='Sort by field')
@click.option('--limit', type=int, default=20, help='Number of results to show')
@click.option('--filter', type=str, default='', help='Filter by keyword')
def unfollowers(sort: str, limit: int, filter: str):
    """Show people who follow you but you don't follow back"""
    try:
        analyzer = _load_analyzer()
        if not analyzer:
            return
        
        one_way = analyzer.get_one_way_followers()
        
        if filter:
            one_way = analyzer.filter_by_keyword(one_way, filter)
        
        if not one_way:
            click.echo(click.style("✓ No one-way followers found!", fg='green'))
            return
        
        # Prepare table data
        table_data = []
        for uid, info in list(one_way.items())[:limit]:
            verified = '✓' if info.get('is_verified') else ''
            private = '🔒' if info.get('is_private') else ''
            table_data.append([
                info['username'],
                info.get('full_name', 'N/A'),
                verified,
                private
            ])
        
        headers = ['Username', 'Full Name', 'Verified', 'Private']
        
        click.echo(click.style(f"\n👥 People who follow you but you don't follow back ({len(one_way)} total)", fg='cyan'))
        click.echo(tabulate(table_data, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg='red'))


@cli.command()
@click.option('--limit', type=int, default=20, help='Number of results to show')
@click.option('--filter', type=str, default='', help='Filter by keyword')
def notfollowingback(limit: int, filter: str):
    """Show people you follow but who don't follow back"""
    try:
        analyzer = _load_analyzer()
        if not analyzer:
            return
        
        one_way = analyzer.get_one_way_following()
        
        if filter:
            one_way = analyzer.filter_by_keyword(one_way, filter)
        
        if not one_way:
            click.echo(click.style("✓ No one-way following found!", fg='green'))
            return
        
        # Prepare table data
        table_data = []
        for uid, info in list(one_way.items())[:limit]:
            verified = '✓' if info.get('is_verified') else ''
            private = '🔒' if info.get('is_private') else ''
            table_data.append([
                info['username'],
                info.get('full_name', 'N/A'),
                verified,
                private
            ])
        
        headers = ['Username', 'Full Name', 'Verified', 'Private']
        
        click.echo(click.style(f"\n👥 People you follow but who don't follow back ({len(one_way)} total)", fg='cyan'))
        click.echo(tabulate(table_data, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg='red'))


@cli.command()
@click.option('--limit', type=int, default=20, help='Number of results to show')
def mutual(limit: int):
    """Show people who follow you and you follow back"""
    try:
        analyzer = _load_analyzer()
        if not analyzer:
            return
        
        mutuals = analyzer.get_mutual_followers()
        
        if not mutuals:
            click.echo(click.style("✗ No mutual followers found!", fg='yellow'))
            return
        
        # Prepare table data
        table_data = []
        for uid, (follower_info, following_info) in list(mutuals.items())[:limit]:
            verified = '✓' if follower_info.get('is_verified') else ''
            table_data.append([
                follower_info['username'],
                follower_info.get('full_name', 'N/A'),
                verified
            ])
        
        headers = ['Username', 'Full Name', 'Verified']
        
        click.echo(click.style(f"\n👥 Mutual followers ({len(mutuals)} total)", fg='cyan'))
        click.echo(tabulate(table_data, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg='red'))


@cli.command()
def stats():
    """Show statistics about your followers"""
    try:
        analyzer = _load_analyzer()
        if not analyzer:
            return
        
        stats = analyzer.get_statistics()
        summary = analyzer.export_comparison_summary()
        
        # Main statistics
        stats_data = [
            ['Total Followers', stats.total_followers],
            ['Total Following', stats.total_following],
            ['Mutual Follows', stats.mutual_follows],
            ['One-Way Followers', stats.one_way_followers],
            ['One-Way Following', stats.one_way_following],
            ['Engagement Ratio', f"{stats.engagement_ratio}%"],
            ['Follow-Back Ratio', f"{stats.follow_back_ratio}%"],
        ]
        
        click.echo(click.style("\n📊 Follower Statistics\n", fg='cyan', bold=True))
        click.echo(tabulate(stats_data, headers=['Metric', 'Value'], tablefmt='grid'))
        
        # Additional insights
        click.echo(click.style("\n🔍 Additional Insights\n", fg='cyan', bold=True))
        insights_data = [
            ['Verified Followers', summary['verified_followers']],
            ['Private Followers', summary['private_followers']],
            ['Potentially Inactive', summary['inactive_followers']],
        ]
        
        click.echo(tabulate(insights_data, headers=['Category', 'Count'], tablefmt='grid'))
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg='red'))


@cli.command()
def export():
    """Export analysis to JSON file"""
    try:
        analyzer = _load_analyzer()
        if not analyzer:
            return
        
        # Create export data
        export_data = {
            'summary': analyzer.export_comparison_summary(),
            'one_way_followers': {
                str(uid): info 
                for uid, info in analyzer.get_one_way_followers().items()
            },
            'one_way_following': {
                str(uid): info 
                for uid, info in analyzer.get_one_way_following().items()
            },
            'mutual_followers': {
                str(uid): str(info[0]['username']) 
                for uid, info in analyzer.get_mutual_followers().items()
            }
        }
        
        # Save to file
        filename = os.path.join(Config.CACHE_DIR, 'analysis_export.json')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        click.echo(click.style(f"✓ Analysis exported to {filename}", fg='green'))
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg='red'))


def _load_analyzer() -> FollowerAnalyzer or None:
    """
    Load cached follower and following data and create analyzer
    
    Returns:
        FollowerAnalyzer or None
    """
    cache_dir = Config.CACHE_DIR
    
    # Find latest cache files
    followers_files = [f for f in os.listdir(cache_dir) if f.endswith('_followers_*.json')]
    following_files = [f for f in os.listdir(cache_dir) if f.endswith('_following_*.json')]
    
    if not followers_files or not following_files:
        click.echo(click.style("✗ No cached data found. Please run 'fetch' command first:", fg='red'))
        click.echo("  instagram-analyzer fetch")
        return None
    
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
    
    return FollowerAnalyzer(followers, following)


if __name__ == '__main__':
    cli()

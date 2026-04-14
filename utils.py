"""
Utility functions for Instagram Follower Analyzer
"""
import json
import csv
from typing import Dict, List
from pathlib import Path
from datetime import datetime


class DataExporter:
    """Export analysis data in various formats"""
    
    @staticmethod
    def to_csv(data: Dict[int, Dict], filename: str, fields: List[str] = None) -> str:
        """
        Export data to CSV file
        
        Args:
            data: Dictionary of user data
            filename: Output CSV filename
            fields: Fields to include (default: all)
            
        Returns:
            str: Path to created file
        """
        if not data:
            raise ValueError("No data to export")
        
        # Get fields from first entry if not specified
        if not fields and data:
            sample = list(data.values())[0]
            fields = list(sample.keys())
        
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for user_data in data.values():
                writer.writerow({field: user_data.get(field, '') for field in fields})
        
        return str(filepath)
    
    @staticmethod
    def to_json(data: Dict, filename: str, pretty: bool = True) -> str:
        """
        Export data to JSON file
        
        Args:
            data: Data to export
            filename: Output JSON filename
            pretty: Pretty print JSON (default: True)
            
        Returns:
            str: Path to created file
        """
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                json.dump(data, f, ensure_ascii=False)
        
        return str(filepath)
    
    @staticmethod
    def to_html_report(analyzer, filename: str) -> str:
        """
        Generate an HTML report
        
        Args:
            analyzer: FollowerAnalyzer instance
            filename: Output HTML filename
            
        Returns:
            str: Path to created file
        """
        from follower_analyzer import FollowerAnalyzer
        
        stats = analyzer.get_statistics()
        summary = analyzer.export_comparison_summary()
        
        html = f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Instagram Analiz Raporu</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f0f2f5; padding: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 30px; }}
                h1 {{ color: #1a1a1a; margin-bottom: 10px; }}
                .subtitle {{ color: #666; font-size: 14px; margin-bottom: 30px; }}
                h2 {{ color: #1a1a1a; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #0095f6; padding-bottom: 10px; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
                .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
                .stat-card.blue {{ background: linear-gradient(135deg, #0095f6 0%, #007ee5 100%); }}
                .stat-card.green {{ background: linear-gradient(135deg, #31a24c 0%, #2d8c45 100%); }}
                .stat-card.red {{ background: linear-gradient(135deg, #e0245e 0%, #c4165c 100%); }}
                .stat-value {{ font-size: 32px; font-weight: bold; margin: 10px 0; }}
                .stat-label {{ font-size: 14px; opacity: 0.9; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #f8f9fa; font-weight: 600; color: #1a1a1a; }}
                tr:hover {{ background: #f8f9fa; }}
                .icon {{ margin-right: 5px; }}
                .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #999; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Instagram Takipçi Analizi Raporu</h1>
                <p class="subtitle">Hazırlanma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
                
                <h2>📈 Ana İstatistikler</h2>
                <div class="stats-grid">
                    <div class="stat-card blue">
                        <div class="stat-label">Toplam Takipçi</div>
                        <div class="stat-value">{stats.total_followers:,}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Takip Edilen</div>
                        <div class="stat-value">{stats.total_following:,}</div>
                    </div>
                    <div class="stat-card green">
                        <div class="stat-label">Karşılıklı Takip</div>
                        <div class="stat-value">{stats.mutual_follows:,}</div>
                    </div>
                    <div class="stat-card red">
                        <div class="stat-label">Tek Yönlü Takipçi</div>
                        <div class="stat-value">{stats.one_way_followers:,}</div>
                    </div>
                </div>
                
                <h2>📊 Detaylı Metrikler</h2>
                <table>
                    <tr>
                        <th>Metrik</th>
                        <th>Değer</th>
                    </tr>
                    <tr>
                        <td>Toplam Takipçi</td>
                        <td>{stats.total_followers:,}</td>
                    </tr>
                    <tr>
                        <td>Toplam Takip Edilen</td>
                        <td>{stats.total_following:,}</td>
                    </tr>
                    <tr>
                        <td>Karşılıklı Takipçiler</td>
                        <td>{stats.mutual_follows:,}</td>
                    </tr>
                    <tr>
                        <td>Tek Yönlü Takipçiler</td>
                        <td>{stats.one_way_followers:,}</td>
                    </tr>
                    <tr>
                        <td>Siz Takip Ettiğiniz Ama Takip Etmeyen</td>
                        <td>{stats.one_way_following:,}</td>
                    </tr>
                    <tr>
                        <td>Engagement Oranı</td>
                        <td>{stats.engagement_ratio}%</td>
                    </tr>
                    <tr>
                        <td>Geri Dönüş Oranı</td>
                        <td>{stats.follow_back_ratio}%</td>
                    </tr>
                </table>
                
                <h2>🔍 Ek İçgörüler</h2>
                <table>
                    <tr>
                        <th>Kategori</th>
                        <th>Sayı</th>
                    </tr>
                    <tr>
                        <td>✓ Doğrulanmış Takipçiler</td>
                        <td>{summary['verified_followers']}</td>
                    </tr>
                    <tr>
                        <td>🔒 Özel Hesaplar</td>
                        <td>{summary['private_followers']}</td>
                    </tr>
                    <tr>
                        <td>⚠️ Potansiyel Inaktif Hesaplar</td>
                        <td>{summary['inactive_followers']}</td>
                    </tr>
                </table>
                
                <div class="footer">
                    <p>Bu rapor Instagram Follower Analyzer tarafından oluşturulmuştur.</p>
                    <p>Rapor yalnızca kişisel kullanım için tasarlanmıştır.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(filepath)


class DataAnalyzer:
    """Advanced analysis functions"""
    
    @staticmethod
    def get_most_followed(data: Dict[int, Dict], limit: int = 10) -> List[tuple]:
        """Get most followed accounts from a list"""
        # This would need follower counts from API
        return []
    
    @staticmethod
    def find_dormant_accounts(followers: Dict, following: Dict, threshold_days: int = 30) -> Dict:
        """
        Find potentially dormant accounts
        (This would need timestamp data from API)
        """
        return {}
    
    @staticmethod
    def get_follow_patterns(followers: Dict, following: Dict) -> Dict:
        """Analyze follow patterns"""
        patterns = {
            'highly_followed': len([f for f in followers.values() if f.get('is_verified')]),
            'private_accounts': len([f for f in followers.values() if f.get('is_private')]),
            'ghost_followers': len([f for f in followers.values() if not f.get('full_name')])
        }
        return patterns

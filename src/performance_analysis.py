import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import logging

class PerformanceAnalyzer:
    def __init__(self, video_data, face_data):
        self.video_data = video_data
        self.face_data = face_data

    def calculate_influencer_performance(self):
        self.video_data = self.video_data.rename(columns={'Video URL': 'video'})

        print(self.video_data.keys())
        print(self.face_data.keys())

        merged_data = pd.merge(
            self.video_data, 
            self.face_data, 
            on='video', 
            how='inner'
        )

        influencer_performance = merged_data.groupby('face_encoding').agg({
            'Performance': ['mean', 'count'],
            'video': 'first'
        }).reset_index()

        influencer_performance.columns = [
            'face_encoding', 
            'avg_performance', 
            'video_count', 
            'sample_video'
        ]

        return influencer_performance

    def identify_top_performers(self, min_videos=3):
        performance = self.calculate_influencer_performance()
        
        # Filter influencers with minimum video count
        top_performers = performance[
            performance['video_count'] >= min_videos
        ].sort_values('avg_performance', ascending=False)
        
        return top_performers
    
class PerformanceMetrics:
    def __init__(self, data: pd.DataFrame):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        self._validate_input_data(data)
        self.data = data
        
        self.performance_columns = [
            'views', 'likes', 'comments', 'shares', 
            'engagement_rate', 'watch_time'
        ]

    def _validate_input_data(self, data: pd.DataFrame):
        required_columns = [
            'video_id', 'influencer_id', 
            'views', 'likes', 'comments', 
            'shares', 'video_duration'
        ]
        
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"Missing required column: {col}")
        
        numeric_columns = ['views', 'likes', 'comments', 'shares', 'video_duration']
        if (data[numeric_columns] < 0).any().any():
            raise ValueError("Negative values found in performance metrics")

    def calculate_engagement_rate(self) -> pd.DataFrame:
        try:
            self.data['engagement_rate'] = (
                (self.data['likes'] + 
                 self.data['comments'] * 1.5 +   
                 self.data['shares'] * 2.0)  
                / self.data['views'] * 100
            )
            
            return self.data[['video_id', 'influencer_id', 'engagement_rate']]
        
        except Exception as e:
            self.logger.error(f"Error calculating engagement rate: {e}")
            raise

    def aggregate_influencer_performance(self, 
                                         metrics: Optional[list] = None,
                                         min_videos: int = 3) -> pd.DataFrame:
        if metrics is None:
            metrics = [
                'views', 'likes', 'comments', 
                'shares', 'engagement_rate'
            ]
        
        influencer_performance = self.data.groupby('influencer_id').agg({
            **{metric: ['mean', 'median', 'max'] for metric in metrics},
            'video_id': 'count'
        }).reset_index()
        
        influencer_performance.columns = (
            ['influencer_id'] + 
            [f'{metric}_{agg}' for metric in metrics for agg in ['mean', 'median', 'max']] + 
            ['total_videos']
        )
        
        influencer_performance = influencer_performance[
            influencer_performance['total_videos'] >= min_videos
        ]
        
        return influencer_performance

    def identify_top_performers(self, 
                                ranking_metric: str = 'engagement_rate_mean', 
                                top_n: int = 10) -> pd.DataFrame:
        performance = self.aggregate_influencer_performance()
        
        # Sort and select top performers
        top_performers = performance.nlargest(top_n, ranking_metric)
        
        return top_performers

    def performance_consistency_analysis(self) -> pd.DataFrame:
        consistency_metrics = self.data.groupby('influencer_id').agg({
            'engagement_rate': ['mean', 'std'],
            'video_id': 'count'
        }).reset_index()
        
        consistency_metrics['engagement_consistency'] = (
            consistency_metrics[('engagement_rate', 'std')] / 
            consistency_metrics[('engagement_rate', 'mean')] * 100
        )
        
        consistency_metrics.columns = [
            'influencer_id', 'engagement_mean', 
            'engagement_std', 'total_videos', 
            'engagement_consistency'
        ]
        
        return consistency_metrics

    def generate_performance_report(self) -> Dict[str, Any]:
        report = {
            'top_performers': self.identify_top_performers(),
            'performance_consistency': self.performance_consistency_analysis(),
            'overall_metrics': {
                'total_influencers': self.data['influencer_id'].nunique(),
                'total_videos': len(self.data),
                'average_engagement_rate': self.data['engagement_rate'].mean()
            }
        }
        
        return report

def load_performance_data(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path, 
                         dtype={
                             'video_id': str, 
                             'influencer_id': str
                         },
                         parse_dates=['video_date'])
        
        return df
    
    except Exception as e:
        logging.error(f"Error loading performance data: {e}")
        raise

def main():
    
    performance_data = load_performance_data('data/processed/performance_data.csv')
    
    metrics_analyzer = PerformanceMetrics(performance_data)
    
    metrics_analyzer.calculate_engagement_rate()
    
    performance_report = metrics_analyzer.generate_performance_report()
    
    top_performers = performance_report['top_performers']
    top_performers.to_csv('reports/top_performers.csv', index=False)
    
    logging.info(f"Performance Report Overview:")
    logging.info(f"Total Influencers: {performance_report['overall_metrics']['total_influencers']}")
    logging.info(f"Total Videos: {performance_report['overall_metrics']['total_videos']}")
    logging.info(f"Average Engagement Rate: {performance_report['overall_metrics']['average_engagement_rate']:.2f}%")

if __name__ == '__main__':
    main()
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class PerformanceVisualizer:
    def __init__(self, performance_data):
        self.data = performance_data

    def plot_performance_distribution(self, output_path='reports/performance_dist.png'):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.data['avg_performance'], kde=True)
        plt.title('Distribution of Influencer Performance')
        plt.xlabel('Average Performance')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def plot_top_performers(self, top_n=10, output_path='reports/top_performers.png'):
        top_performers = self.data.nlargest(top_n, 'avg_performance')
        
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x='sample_video', 
            y='avg_performance', 
            data=top_performers
        )
        plt.title(f'Top {top_n} Influencers by Performance')
        plt.xlabel('Sample Video')
        plt.ylabel('Average Performance')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
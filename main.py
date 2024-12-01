import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_retrieval import DataRetriever
from src.face_detection import InfluencerDetector
from src.performance_analysis import PerformanceAnalyzer
from src.visualization import PerformanceVisualizer

def main():
    # 1. Retrieve Data
    data_retriever = DataRetriever("./cred2.json")
    
    video_data = data_retriever.get_data()
    data_retriever.save_data(video_data)

    # 2. Detect Influencers
    influencer_detector = InfluencerDetector()
    # face_data = influencer_detector.process_videos()
    # face_data.to_csv('reports/face_data.csv', index=False)

    # read face data from file
    face_data = pd.read_csv('reports/updated_face_data.csv')

    # 3. Analyze Performance
    performance_analyzer = PerformanceAnalyzer(video_data, face_data)
    influencer_performance = performance_analyzer.identify_top_performers()

    # 4. Visualize Results
    visualizer = PerformanceVisualizer(influencer_performance)
    visualizer.plot_performance_distribution()
    visualizer.plot_top_performers()

    # 5. Save Results
    influencer_performance.to_csv('reports/influencer_performance.csv', index=False)

if __name__ == '__main__':
    main()
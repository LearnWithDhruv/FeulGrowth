
# Influencer Performance Analysis

This project is designed to analyze the performance of influencers by retrieving and processing video data, detecting faces, and performing analytics. The results are visualized for insights into influencer engagement and effectiveness.

## Project Directory Structure

```
influencer-performance-analysis/
│
├── data/
│   └── processed/
│       └── performance_data.csv
│── reports/ 
│   ├── face_data.csv
│   ├── influencer_performance.csv
│   ├── performance_dist.png
│   └── top_performers.png
    └── updated_face_data.png
│       
├── src/
│   ├── __init__.py
│   ├── data_retrieval.py
│   ├── face_detection.py
│   ├── performance_analysis.py
│   └── visualization.py
│
├── requirements.txt
├── README.md
└── main.py
├── download.py
├── rename.py
└── setup.py

```

## Directory Details

### `data/`
- **raw/videos/**: Contains raw video files for analysis.
- **processed/performance_data.csv**: Processed data results stored in a CSV format.

### `src/`
- **data_retrieval.py**: Scripts to retrieve data (e.g., downloading videos or loading files).
- **face_detection.py**: Implements face detection logic in video frames.
- **performance_analysis.py**: Analyzes influencer performance metrics.
- **visualization.py**: Generates visualizations from the analyzed data.
- **__init__.py**: Marks the directory as a Python package.

`performance_analysis.py`.

### `requirements.txt`
Contains a list of Python dependencies required to run the project.

### `README.md`
This documentation file describing the project.

### `main.py`
Entry point of the project, orchestrating the modules for influencer performance analysis.

## How to Use

1. **Setup the Environment**:
   - Install dependencies using: 
     ```bash
     pip install -r requirements.txt
     ```

2. **Add Raw Data**:
   - Place video files in the `data/raw/videos/` directory.

3. **Run the Project**:
   - Execute the `main.py` script to perform the analysis:
     ```bash
     python main.py
     ```

4. **View Results**:
   - Processed data will be stored in `data/processed/performance_data.csv`.
   - Visualizations will be generated in the appropriate format.

5. **Explore Data**:
   - Use `notebooks/exploratory_analysis.ipynb` for custom analysis.

## Testing
Run the tests to ensure functionality:
```bash
pytest tests/
```

## Contributions
Feel free to contribute by submitting issues or pull requests.

## License
This project is licensed under the [MIT License](LICENSE).

---
**Note**: Replace this placeholder license section with your actual license if different.

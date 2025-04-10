# Sanaad Pro Analytics

## Overview

**Sanaad Pro Analytics** is an intelligent, integrated system designed to enhance athletic performance while prioritizing injury prevention. Leveraging artificial intelligence, Sanaad analyzes athletes' movements, delivering personalized recommendations to boost performance and reduce injury risks. It also supports the development of smart training programs to improve skills and tracks progress during rehabilitation post-injury.

## Features
1. **Injury Risk Analysis**: Evaluates risks based on metrics like fatigue, heart rate, tackles, and hydration.
2. **Interactive Field Map**: Displays player positions with performance details on hover.
3. **Player Performance Dashboard**: Compares individual performance to team averages.
4. **Formal Design**: Clean, professional interface with muted, official colors.

## Prerequisites
To run Sanaad Pro Analytics, ensure you have the following:
- **Python**: Version 3.8 or higher
- **Git**: For cloning the repository (optional if downloading manually)
- **pip**: Python package manager (usually included with Python)
- A modern web browser (e.g., Chrome, Firefox)

## Installation
Follow these steps to set up the project on your local machine:

1. **Clone the Repository** (or download manually):
   ```bash
   git clone https://github.com/username/sanaad-pro-analytics.git
   cd sanaad-pro-analytics

Note: Replace username with your GitHub username. If you don’t use Git, download the ZIP file from GitHub and extract it.

2. Set Up a Virtual Environment (optional but recommended):

```bash
 python -m venv venv
 source venv/bin/activate  # On Linux/Mac
 venv\Scripts\activate     # On Windows
```


This isolates the project’s dependencies from your system Python.
3. Install Required Libraries:
    Ensure you have a requirements.txt file with the following content:
    ```
streamlit==1.36.0
plotly==5.22.0
pandas==2.2.2
numpy==1.26.4
    ```

4. Run the installation command:

```bash
pip install -r requirements.txt
```

## Running the Program

### After installation, follow these steps to launch the application:

- Prepare the Data File:
        Ensure a file named player_data_realistic.json exists in the project directory.
        This file contains player data (see "Data Format" section below). If missing, the app will display an error.
- Launch the Application:
  ```bash
  streamlit run s.py
  ```
  Access the App:

- Open your web browser and go to: http://localhost:8501.
- The app will load, displaying the Sanaad Pro Analytics interface.

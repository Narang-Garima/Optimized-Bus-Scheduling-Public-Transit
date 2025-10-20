# Optimized Bus Scheduling for Public Transit

This project applies operations research techniques to optimize public bus network scheduling. It focuses on addressing inefficiencies in static schedules and incorporates real-world factors such as traffic delays and environmental impact.

## Project Overview

Urban public transit systems often suffer from outdated and rigid scheduling that fails to align with real-time passenger demand. This project uses Python and Google OR-Tools to build:

- A Baseline Model: Minimizes waiting time and bus deployment cost.
- An Extended Model: Includes traffic delay and CO₂ emissions to reflect realistic scheduling scenarios.

## Objectives

- Minimize passenger waiting time.
- Optimize bus count to reduce operational cost.
- Balance environmental and service quality goals.

## Methodology

- Data: Synthetic data for hourly demand and traffic delays.
- Tools and Libraries: Python, OR-Tools, NumPy, Matplotlib, Streamlit, Pandas, and Folium.
- Approach:
  - Constraint programming for schedule optimization.
  - Visualization of waiting time and emissions.
  - Route mapping using Folium.

## Features

- Streamlit-based interactive dashboard.
- Comparison between baseline and extended scheduling models.
- Visual insights on emissions and operational efficiency.
- Interactive route map displaying sample bus stops.

## How to Run

### Prerequisites

1. Install the required Python packages:
  pip install ortools streamlit streamlit-folium numpy pandas matplotlib folium

2. Running in PyCharm or Terminal

3. Open the project folder in PyCharm.

4. Make sure your Python environment is activated.

5. Open the terminal inside PyCharm (bottom panel) or your system terminal.

6. Navigate to the directory where bus_scheduling.py is located.

7. Run the following command:
    streamlit run bus_scheduling.py

    A browser window will automatically open with the app. If not, copy and paste the link shown in the terminal into your browser.





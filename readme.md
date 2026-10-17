# Global Dollar Shortage Simulator 💵

An interactive macro-finance sandbox built with Streamlit. This app simulates how global funding shocks—such as lost export receipts and refinancing freezes—cascade down into firm-level liquidity risk.

## Features
* **Global Shock Stress Testing**: Adjust absolute USD export losses and refinancing availability to see real-time impacts.
* **Balance Sheet Visualization**: Stacked bar charts comparing obligations versus available resources.
* **Tipping Point Analysis**: Line charts illustrating rollover stress and funding gaps.
* **Comparative Company Profiles**: Compare the vulnerability of an exporter (Company A) versus a domestic seller (Company B).

## Installation

Follow these steps to get the simulator running on your local machine:

**1. Clone the repository**
Open your terminal and clone this project to your local machine:
```bash
git clone https://github.com/your-username/dollar-shortage-simulator.git
cd dollar-shortage-simulator
```

**2. Set up a virtual environment (Recommended)**
It is best practice to create a virtual environment to keep dependencies separate.
* For Windows:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* For macOS/Linux:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

**3. Install dependencies**
Install the required Python packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Usage

Once everything is installed, run the Streamlit app from your terminal:
```bash
streamlit run model.py
```

The application will automatically open in your default web browser (typically at `http://localhost:8501`). Use the sidebar sliders to interact with the model and stress-test the corporate balance sheets.

## Disclaimer
This is an educational model and not a financial forecasting tool. All values are illustrative.
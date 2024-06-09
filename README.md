# CSVProcessor

CSVProcessor is a Django-based web application that allows users to upload CSV files, perform data preprocessing operations,
and visualize the results. It integrates with Pandas, Seaborn, and Matplotlib for data manipulation and visualization.

## Description

CSVProcessor is designed to help users:
- Upload and manage CSV files.
- Perform various data preprocessing tasks such as handling missing data, calculating statistical measures(Mean, Median and Standard Deviation), and more.
- Visualize data using heatmaps, histograms, scatter plot matrices, and violin plots.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)


## Installation

### Prerequisites

- Python 3.8 or higher
- Django
- Pandas
- Seaborn
- Matplotlib



### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/CSVProcessor.git
    ```

2. Navigate to the project directory:
    ```sh
    cd CSVProcessor
    ```

3. Install the required dependencies:
    ```sh
    pip install django,pandas,seaborn,matplotlib (Python is necessary to be installed globally to be able to run pip commands)
    ```

4. Apply migrations:
    ```sh
    python manage.py migrate
    ```

5. Start the Django development server:
    ```sh
    python manage.py runserver
    ```

   After these steps the django application will open -> Starting development server at http://127.0.0.1:8000/ where you can view the application.
  # A note to make , perform the operations one by one and not all together. Thank you  

Example snapshots are in the folder named "snapshots"
Sample CSV File is provided in the "sample CSV" folder .

   

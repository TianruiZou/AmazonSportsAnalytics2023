Amazon Sports Analytics 2023
This project focuses on analyzing sports-related product data from Amazon UK, aiming to uncover trends, pricing strategies, and other key performance insights through data cleaning, exploration, and advanced analysis.

Project Overview
Using real-world data scraped from Amazon UK in October 2023, this project provides insights into product categories, pricing distribution, and potential predictors of product success. The goal is to demonstrate end-to-end data analysis capabilities using Python and commonly used data science libraries.

Dataset
Source: https://www.kaggle.com/datasets/asaniczka/amazon-uk-products-dataset-2023?resource=download

Size: Over 2.2 million records

Fields: Product name, category, brand, price, rating, review count, and more.

Project Structure
. ├── data/
│ ├── raw/ # Original dataset (not included due to size)
│ └── processed/ # Cleaned and prepared data
├── notebooks/
│ ├── data_cleaning.ipynb # Data preprocessing and cleaning
│ ├── exploratory_analysis.ipynb # Exploratory Data Analysis (EDA)
│ └── advanced_analysis.ipynb # Feature analysis / modeling
├── outputs/ # Visualizations and summary images
├── src/
│ ├── data_cleaning.py # Python scripts for data wrangling
│ ├── data_visualization.py # Visuals generation
│ └── advanced_analysis.py # Advanced analysis / modeling
├── requirements.txt # Project dependencies
└── README.md # Project documentation

How to Run the Project
Clone the repository:

git clone https://github.com/TianruiZou/AmazonSportsAnalytics2023.git

(Optional) Create a virtual environment:

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

Install required packages:

pip install -r requirements.txt

Run the analysis notebooks:

Open Jupyter and start from notebooks/data_cleaning.ipynb.

Technologies Used
Language: Python 3

Libraries:

pandas, numpy (data processing)

matplotlib, seaborn (data visualization)

scikit-learn (machine learning)

Jupyter Notebook (analysis interface)

Key Analysis Steps
Data Cleaning:

Removed duplicates and handled missing values

Standardized price and rating formats

Exploratory Data Analysis:

Analyzed pricing trends, category distributions, and product popularity

Visualized review scores, brand prevalence, and more

Advanced Analysis:

Identified high-performing categories

Explored potential correlations between price, ratings, and sales estimates

Sample Visualizations
Here are a few examples of insights produced in this project:

(Figure 1: Sales trend across top product categories)
(Figure 2: Product price distribution – log scale)

Note: Images should be saved in the outputs/ directory and linked here.

License
This project is licensed under the MIT License. See the LICENSE file for more information.

Acknowledgments
Kaggle dataset author: @asaniczka

Thanks to the open-source community and Python ecosystem that made this project possible.

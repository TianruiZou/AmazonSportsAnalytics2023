# Amazon Product Data Analysis

This project analyzes Amazon product data with a focus on sports and outdoor products. It includes data cleaning, visualization, and advanced analysis of product performance metrics.

## Project Structure

```
.
├── analyze_csv.py          # CSV file analysis
├── check_categories.py     # Category checking
├── clean_and_save_data.py  # Data cleaning and saving
├── clean_data.py          # Basic data cleaning
├── further_clean_data.py  # Advanced data cleaning
├── merge_excel_files.py   # Excel file merging
├── sport_analysis.py      # Sports product analysis
├── sport_advanced_analysis.py  # Advanced sports product analysis
└── visualization_analysis.py   # Data visualization
```

## Features

- Data cleaning and preprocessing
- Product category analysis
- Sales performance visualization
- Rating distribution analysis
- Price range analysis
- Advanced statistical analysis
- Composite scoring system

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- openpyxl

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/amazon-product-analysis.git
cd amazon-product-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Data Preparation:
```bash
python merge_excel_files.py
python clean_data.py
python further_clean_data.py
python clean_and_save_data.py
```

2. Analysis:
```bash
python visualization_analysis.py
python sport_analysis.py
python sport_advanced_analysis.py
```

3. Verification:
```bash
python check_categories.py
python analyze_csv.py
```

## Output

All analysis results and visualizations are saved in the `output/` directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 
ORGANISATION DATA PROCESSING SYSTEM
===================================

General Statistical Data Analysis Platform


1. PROJECT DESCRIPTION
----------------------

Organisation Data Processing System is a general statistical data
processing and analysis platform developed using Python and Streamlit.

The system provides a user-friendly interface for uploading, cleaning,
validating, analysing, visualising, extracting and calculating data
without requiring users to write statistical programming code.

Although the original project was designed with an organisation and
department-oriented concept, the current version has been developed as
a general statistical analysis platform that can be used with different
types of datasets.


2. MAIN FEATURES
----------------

The current version includes:

- Data Upload
- Data Preview
- Data Information
- Data Cleaning
- Missing Values Handling
- Duplicate Detection and Removal
- Column Name Standardisation
- Empty Column Detection
- Data Type Validation
- Numeric Data Stored as Text Detection
- Descriptive Statistics
- Frequency Analysis
- Distribution Analysis
- Correlation Analysis
- Outlier Detection
- Dashboard and Data Visualisation
- Data Extraction and Filtering
- User-Defined Data Calculation
- Calculated Data Extraction
- Processing Reports
- Processing History
- CSV and Excel Export
- Visitor Information
- Developer Information


3. STATISTICAL METHODS
----------------------

The system currently implements the following statistical and
data-processing methods:

Data Cleaning:
- Missing value detection and treatment
- Duplicate record detection
- Column standardisation
- Data type validation
- Numeric conversion

Descriptive Statistics:
- Count
- Mean
- Median
- Mode
- Minimum
- Maximum
- Range
- Variance
- Standard Deviation
- Quartiles (Q1, Q2, Q3)

Frequency and Distribution:
- Frequency tables
- Percentage distributions
- Cumulative frequency
- Cumulative percentage
- Grouped frequency distribution
- Histogram analysis

Correlation:
- Pearson correlation coefficient
- Correlation matrix
- Correlation heatmap
- Correlation strength classification
- Positive and negative relationship identification

Outlier Detection:
- Interquartile Range (IQR) method
- Q1 and Q3 calculation
- Lower and upper outlier bounds
- Outlier identification
- Outlier percentage
- Box plot visualisation

Data Extraction:
- Column selection
- Row filtering
- Multiple filtering rules
- AND / OR conditions
- Numeric, text and date conditions
- Missing and non-missing conditions

User-Defined Calculation:
- Addition
- Subtraction
- Multiplication
- Division
- Power
- Modulo
- Parentheses
- Mathematical functions such as:
  abs(), round(), sqrt(), log(), log10(), exp()


4. TECHNOLOGY STACK
-------------------

Programming Language:
- Python

Application Framework:
- Streamlit

Data Processing:
- Pandas

Statistical/Data Analysis:
- Pandas statistical functions
- NumPy functionality through the Python data-analysis ecosystem

Data Visualisation:
- Matplotlib
- Streamlit charts

Excel Processing:
- OpenPyXL

File Formats:
- CSV
- XLSX


5. DEVELOPMENT APPROACH
-----------------------

The application was developed using a modular and version-based approach.

Each major version was developed and tested independently before
proceeding to the next version.

The development process included:

1. Data upload
2. Data cleaning and validation
3. Statistical analysis
4. Data visualisation
5. Data extraction
6. User-defined calculations
7. Calculated-data extraction
8. Testing and error correction
9. Final integration


6. PROJECT VERSIONS
-------------------

V1 - Data Upload, Cleaning and Validation
- Data upload
- Data preview
- Data cleaning
- Data validation
- Cleaning reports
- Data download

V2.1 - Descriptive Statistics
- Descriptive statistical measures
- Variable-level analysis
- Quartile analysis
- Statistical result downloads

V2.2 - Frequency and Distribution Analysis
- Categorical frequency analysis
- Numeric grouped frequency distribution
- Histograms
- Distribution summaries

V2.3 - Correlation Analysis
- Pearson correlation
- Correlation matrix
- Heatmap
- Correlation interpretation

V2.4 - Outlier Detection
- IQR-based outlier detection
- Outlier summaries
- Box plots
- Outlier downloads

V3 - Dashboard and Visualisation
- Statistical dashboard
- Data quality indicators
- Distribution visualisation
- Categorical visualisation
- Correlation visualisation
- Outlier visualisation
- Scatter plots
- Variable comparison
- Time-series/line charts
- Trend analysis

V5.1 - Data Extraction and Filtering
- Rule-based data extraction
- Multiple filtering conditions
- AND / OR filtering
- CSV and Excel export

V5.2 - User-Defined Data Calculation
- User-defined mathematical expressions
- Safe expression processing
- Generated variables
- Calculation results

V5.3 - Calculated Data Extraction
- Filtering calculated variables
- Generated-variable extraction
- Optional working-dataset update
- CSV and Excel export


7. PROJECT STRUCTURE
--------------------

OrganisationDataApp/
|
|-- app.py
|
|-- pages/
|   |-- app2.py
|   |-- dep.py
|   |-- xtract.py
|   |-- cal.py
|   |-- extract_calc.py
|   |-- visitor.py
|   |-- developers.py
|
|-- assets/
|   |-- muhammad.jpg
|   |-- abdulrahman.jpg
|   |-- abubakar.jpg
|
|-- venv/
|
|-- README.txt


8. APPLICATION ARCHITECTURE
---------------------------

The application uses Streamlit's multi-page application structure.

The main application handles:
- Data upload
- Data cleaning
- Validation
- Descriptive statistics
- Frequency analysis
- Correlation analysis
- Outlier detection

Additional modules in the pages directory provide:
- Dashboard and visualisation
- Data extraction
- User-defined calculations
- Calculated-data extraction
- Visitor information
- Developer information

The application uses Streamlit session state to maintain the active
working dataset and processing information during the current session.


9. DATA STORAGE
---------------

The current version operates primarily as a session-based application.

Uploaded and processed data are maintained during the active application
session.

Users are advised to download important datasets and analysis results
before ending the session.

Permanent database storage, user accounts, authentication and persistent
user data management are planned as possible future developments.


10. DEPARTMENT ANALYSIS
-----------------------

Department Analysis is currently under maintenance.

The feature has intentionally been kept dormant because the current
application is designed as a general statistical analysis platform.

It may be reactivated in a future private organisation-oriented version.


11. CURRENT VERSION
-------------------

Application Version:
2.4

Major Development Modules:
V1, V2.1, V2.2, V2.3, V2.4, V3, V5.1, V5.2 and V5.3

Project Status:
Current development scope completed and prepared for deployment/repository
publication.


12. DEVELOPERS
--------------

Muhammad Muhamed
Abdul-rahman-Simai
Abubakar

Data Science Students
East African Statistical Training Centre (EASTC)


13. ACKNOWLEDGEMENT
-------------------

Special appreciation to the consultant, Field Student OCGS 2026,
students and contributors, academic and field contributors, and everyone
who supported the development, testing and improvement of this project.


14. FUTURE DEVELOPMENT
----------------------

Possible future improvements include:

- Database integration
- User authentication
- User accounts
- Persistent data storage
- Advanced statistical tests
- Regression analysis
- Advanced time-series analysis
- Forecasting
- Automated statistical reports
- Advanced dashboards
- Private organisation deployment


15. LICENSE
----------

This project is currently maintained as an academic and development
project. Licensing terms may be added or updated when the project is
formally published.


END OF README
=============
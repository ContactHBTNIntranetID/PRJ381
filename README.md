# PRJ381
This project focuses on building an IoT-based system for real-time monitoring and automation. Using sensors, microcontrollers, and cloud services, it allows remote data access and control, improving efficiency, reducing manual tasks, and enabling smart decision-making.|

## Backend Operations
-Connecting to MongoDB Atlas using a secure connection string embedded in the code. 

-Listing all collections within a specified database (PRJ382_DB by default).

-Fetching documents from any collection within the default database, with optional limits on the number of documents retrieved.

-Displaying documents in a readable, tabular format using the tabulate library for easy inspection and debugging.

## Data Cleaning Operations
1. Handles missing data by offering multiple strategies: dropping rows with missing values or filling missing numeric and categorical data with median and mode, respectively.

2. Detects and removes duplicate records, even when complex data types are present, ensuring data integrity.

3. Identifies and removes outliers using statistical methods such as the interquartile range (IQR) to improve data quality.

4. Provides tools to standardize text formatting, including case normalization and special character removal.

5. Enables syncing of the cleaned dataset back to MongoDB by replacing old records with the new, cleaned data, ensuring the database stays up-to-date.

## 📦Dependencies

Make sure you have Python 3.8+ installed. You’ll also need to install the following Python libraries:

pymongo → for connecting to MongoDB

tabulate → for displaying tabular data neatly

numpy → for numerical computations

statsmodels → for ARIMA time series modeling

matplotlib → for data visualization

### Additionally, the project uses Python’s built-in libraries:

datetime

timedelta

And a custom module:

Connections (must contain the function return_documents)

### To download: 

Use (py -m install pymongo OR python -m install pymongo OR pip -m install pymongo) this is all dependent on your PC

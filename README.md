# PRJ381
This project focuses on building an IoT-based system for real-time monitoring and automation. Using sensors, microcontrollers, and cloud services, it allows remote data access and control, improving efficiency, reducing manual tasks, and enabling smart decision-making.|

## Backend Operations
-Connecting to MongoDB Atlas using a secure connection string embedded in the code. 

-Listing all collections within a specified database (PRJ382_DB by default).

-Fetching documents from any collection within the default database, with optional limits on the number of documents retrieved.

-Displaying documents in a readable, tabular format using the tabulate library for easy inspection and debugging.

## API

### 🛠️ Testing in Postman

    1. Open Postman.

    2. Start your API (Run the file).

    3. Enter one of the endpoints (e.g., http://127.0.0.1:5000/collections/ESP32_data).

    4. Click Send.

    The results will appear in JSON format.

### 🛠️ What needs to be installed

    py -m pip install flask

    py -m pip install pymongo

    py -m pip install bson


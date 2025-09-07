# Python Generators: SQL Database Exercises

This repository contains Python scripts demonstrating the use of **generators** to efficiently interact with a PostgreSQL database. The exercises focus on streaming rows, batch processing, lazy pagination, and memory-efficient aggregate computations.

## Repository Structure

python-generators-0x00/
├── seed.py # Sets up the PostgreSQL database and populates user_data
├── 0-stream_users.py # Generator that streams rows from the database one by one
├── 1-batch_processing.py # Fetches rows in batches and filters users over age 25
├── 2-lazy_paginate.py # Lazily fetches paginated data from the database
├── 3-average_age.py # Computes average age using a generator to reduce memory usage
├── user_data.csv # Sample CSV data to populate the database
├── 0-main.py # Optional: script to test database setup and seeding
├── 1-main.py # Optional: test script for streaming first 6 users
├── 2-main.py # Optional: test script for batch processing
├── 3-main.py # Optional: test script for lazy pagination
└── README.md # This documentation

markdown
Copy code

## Objectives

1. **Database Setup**:  
   - Connect to PostgreSQL server  
   - Create a database `ALX_prodev`  
   - Create table `user_data` with fields:  
     - `user_id` (UUID, Primary Key, Indexed)  
     - `name` (VARCHAR, NOT NULL)  
     - `email` (VARCHAR, NOT NULL, UNIQUE)  
     - `age` (DECIMAL, NOT NULL)  
   - Populate the table from `user_data.csv`

2. **Generators**:  
   - `0-stream_users.py`: Streams rows from the database one by one  
   - `1-batch_processing.py`: Fetches rows in batches and filters users over age 25  
   - `2-lazy_paginate.py`: Lazily loads paginated data one page at a time  
   - `3-average_age.py`: Streams user ages to compute average age efficiently

3. **Efficiency Constraints**:  
   - Each script uses **generators** with `yield`  
   - Loop usage is limited to the constraints specified in the exercises  
   - Avoids loading the entire dataset into memory
**ETL Pipeline for User Login Behavior**

This project sets up an ETL pipeline that reads JSON data containing user login behavior from an AWS SQS queue, transforms the data to mask PII (Personal Identifiable Information), and writes the transformed 
data to a PostgreSQL database. The project uses Docker to run all components locally, including LocalStack for SQS emulation and PostgreSQL.

steps I did: 

●	Need Docker and Docker Compose installed on your machine<br/> 
● Need Python 3.6+ installed on your machine

Create Docker Environment<br/> 
Create a docker-compose.yml<br/> 

Initialize LocalStack with Pre-loaded Data<br/> 
Create an localstack-setup.sh file to initialize the SQS queue and load data 

Initialize PostgreSQL with Pre-created Tables<br/> 
Create an init-db.sql file to initialize the PostgreSQL database with the required tables

Start Docker Containers<br/> 
Run the following command to start the Docker containers<br/> 
**Command**: docker-compose up

Run the ETL Script<br/> 
for etl.py file<br/> 
**Command**: python etl.py

**Thought Process**<br/> 
1.	Docker and LocalStack: Using Docker ensures a consistent environment, making it easy to run the components locally. LocalStack emulates AWS services, allowing us to create an SQS queue without needing an AWS account.
2.	Database Initialization: Pre-loading the PostgreSQL database with the required tables ensures that the ETL process has a consistent schema to write to.
3.	PII Masking: The SHA-256 hashing algorithm is used to mask PII fields (masked _device_id and masked_ip). This ensures that the same input always produces the same hash, allowing data analysts to identify duplicates without revealing the actual PII.
4.	ETL Process: The Python script reads messages from the SQS queue, masks the PII, and writes the transformed data to PostgreSQL. The script uses boto3 for interacting with SQS and psycopg2 for interacting with PostgreSQL.


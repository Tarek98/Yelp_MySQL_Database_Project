# Yelp_Database_Project
A MySQL database using a real Yelp dataset from Kaggle, and a CLI client that communicates with an API making queries to the database, to emulate the Yelp social network's functionality for educational purposes. 

MySQL server (with Yelp database) is run on an Ubuntu VM, and the client (frontend) runs on the main operating system hosting the VM.

## Dependencies
- pip install mysql-connector-python

## Setting up the database (on an ubuntu VM)
- download the dataset from https://www.kaggle.com/yelp-dataset/yelp-dataset/version/6?fbclid=IwAR0vo_87U4QBW8ckjCSmkAaNfAWyvD2eL74GwByyL8eW1ZLOy7R2wbrfrF8#yelp_user.csv
- put the csv files in /var/lib/mysql-files/ on the VM
- run filter_csv_rows.sh on the VM
- run yelp_schema.sql on the VM
- run load_data.sql on the VM

## Running the CLI client (on the host OS)
- set the IP address of the ubuntu VM in yelp_api.py and set the credentials of your SQL user
- run yelp_client.py with no arguments
- for a list of commands type help

# ece356_project
Yelp educational database


## Dependencies

- pip install mysql-connector-python

## Setting up the database
- download the dataset from https://www.kaggle.com/yelp-dataset/yelp-dataset/version/6?fbclid=IwAR0vo_87U4QBW8ckjCSmkAaNfAWyvD2eL74GwByyL8eW1ZLOy7R2wbrfrF8#yelp_user.csv
- put the csv files in /var/lib/mysql-files/ on the VM
- run filter_csv_rows.sh on the VM
- run yelp_schema.sql on the VM
- run load_data.sql on the VM

## Running the CLI
- run yelp_client.py with no arguments
- for a list of commands type help

import pandas as pd
from faker import Faker
import random
from google.cloud import storage
import os

# read IBM data
data = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

# Create a fake data
fake = Faker()
data['Employee_Name'] = [fake.name() for _ in range(len(data))]
data['Employee_id'] = [fake.unique.random_int(min=1000, max=9999) for _ in range(len(data))]
data['Phone Number'] = [fake.phone_number() for _ in range(len(data))]
data['Email'] = [fake.email() for _ in range(len(data))]
data['Password'] = [fake.password() for _ in range(len(data))]


# add teh data to IBM data set
cols = ['Employee_Name','Employee_id','Phone Number','Email','Password'] + [col for col in data.columns if col not in ['Employee_Name','Employee_id','Phone Number','Email','Password']]
data = data[cols]


# Save the data to a CSV file
data.to_csv('employee_data.csv', index=False)

# Upload the data to Google Cloud Storage
def upload_to_gcp(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


# Set the environment variable
bucket_name = "people-analytics-avulli"

# Upload the data to Google Cloud Storage
upload_to_gcp(bucket_name, 'employee_data.csv', 'employee_data.csv')

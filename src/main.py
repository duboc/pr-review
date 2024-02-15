import google.cloud.storage


# Function to create a GCS   

#removed empty spaces   
def create_bucket(bucket_name):
    """Creates a new bucket."""
    # bucket_name = "your-new-bucket-name"
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print(f"Bucket {bucket.name} created")
    return bucket  


# Function to upload a file to GCS

import google.cloud.storage


# Function to create a GCS   

def create_bucket(bucket_name):
    """Creates a new bucket."""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.create_bucket(bucket_name)

    print(f"Bucket {bucket.name} created")

    return bucket  


# Function to upload a file to GCS

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race
    # conditions and data corruptions. The request to upload is aborted if the
    # object's generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

    return blob  
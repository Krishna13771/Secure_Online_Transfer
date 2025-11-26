import boto3
import os
from pathlib import Path

def extract_all_files_from_s3(bucket_name, local_dir='downloads'):
    """Extract all files from S3 bucket to local directory"""
    s3 = boto3.client('s3')
    
    # Create local directory if it doesn't exist
    Path(local_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # List all objects in the bucket
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    local_path = os.path.join(local_dir, key)
                    
                    # Create subdirectories if needed
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    
                    # Download the file
                    print(f"Downloading: {key}")
                    s3.download_file(bucket_name, key, local_path)
        
        print(f"All files extracted to: {local_dir}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    bucket_name = input("Enter S3 bucket name: ")
    extract_all_files_from_s3(bucket_name)
from dotenv import load_dotenv
from minio import Minio
import os

load_dotenv()

from minio.error import S3Error

def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio("localhost:9000",
        access_key=os.environ["ACCESSKEY"],
        secret_key=os.environ["SECRETKEY"],
        secure=False
    )

    # The destination bucket and filename on the MinIO server
    bucket_name = "bronze"


    # Make the bucket if it doesn't exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
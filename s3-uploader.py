import boto3
import os
import logging
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

APP_ID = "my-app-id"
BUCKET_NAME = APP_ID.lower()
REGION = "ap-south-1"
UPLOAD_DIR = "./"  # directory containing files like 2024051910-somefile.txt


def get_s3_client():
    try:
        return boto3.client('s3', region_name=REGION)
    except NoCredentialsError as e:
        logger.error("AWS credentials not found.")
        raise e


def ensure_bucket_exists(s3):
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
        logger.info(f"Bucket exists: {BUCKET_NAME}")
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            logger.warning(f"Bucket not found. Creating: {BUCKET_NAME}")
            s3.create_bucket(
                Bucket=BUCKET_NAME,
                CreateBucketConfiguration={'LocationConstraint': REGION}
            )
        else:
            logger.error(f"Error checking bucket: {e}")
            raise


def upload_files(s3):
    files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".txt") and f[:10].isdigit() and '-' in f]
    if not files:
        logger.warning("No matching log files found.")
        return

    for file in files:
        timestamp = file.split('-')[0]  # e.g. 2024051910
        year, month, day = timestamp[:4], timestamp[4:6], timestamp[6:8]
        key = f"{year}/{month}/{day}/{file}"
        file_path = os.path.join(UPLOAD_DIR, file)

        try:
            s3.upload_file(file_path, BUCKET_NAME, key)
            logger.info(f"Uploaded: {key}")

            os.remove(file_path)
            logger.info(f"Deleted local file: {file}")

        except ClientError as e:
            logger.error(f"Upload failed for {file}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for {file}: {e}")


def main():
    s3 = get_s3_client()
    ensure_bucket_exists(s3)
    upload_files(s3)


if __name__ == "__main__":
    main()

from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
import os

def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "http://localhost:9000",
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
    )

    # Make 'modelmesh-models' bucket if not exist.
    bucket_name = "modelmesh-models"
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
    else:
        print(f"Bucket {bucket_name} already exists")

    # Upload './models/mnist-svm.joblib' (or whatever)
    # as object name to our newly created bucket 'modelmesh-models'.
    client.fput_object(
        bucket_name=bucket_name,
        file_path=f"./model_repo/yolov8n_car/",
    )
    print(f"Model and config are successfully uploaded to bucket '{bucket_name}'.")


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

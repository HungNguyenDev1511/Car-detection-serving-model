from minio import Minio
from minio.error import S3Error


def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "http://localhost:9000",
        access_key="AKIAIOSFODNN7EXAMPLE",
        secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
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
    object_name = "mnist-svm.joblib"
    client.fput_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=f"./models/{object_name}",
    )
    print(f"'{object_name}' is successfully uploaded to bucket '{bucket_name}'.")


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

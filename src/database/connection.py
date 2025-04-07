import boto3
import psycopg2
import os
import sys
import json
from botocore.exceptions import BotoCoreError, ClientError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
SECRET_NAME = os.getenv("DB_SECRET_NAME", "rds-secret")
def get_secret(key):
    try:
        session = boto3.session.Session()
        boto3_client = session.client(
            service_name='secretsmanager',
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        secret_response = boto3_client.get_secret_value(SecretId=SECRET_NAME)
        secret = json.loads(secret_response["SecretString"])
        return {
            "host": secret["host"],
            "dbname": secret["dbname"],
            "username": secret["username"],
            "password": secret["password"],
            "port": secret.get("port", 5432)
        }
    except (BotoCoreError, ClientError) as e:
        print(f"Error retrieving secret from AWS Secrets Manager: {e}")
        return None
    except KeyError as e:
        print(f"Missing expected key in secret: {e}")
        return None

def get_db():
    secret_name = os.getenv("DB_SECRET_NAME", "my-db-secret")
    secret = get_secret(secret_name)
    print(secret)
    if secret:
        # Use credentials from AWS Secrets Manager
        db_host = secret["host"]
        db_name = secret["dbname"]
        db_user = secret["username"]
        db_password = secret["password"]
        db_port = secret["port"]
    else:
        # Fallback to environment variables
        db_host = os.getenv("DB_HOST", "localhost")
        db_name = os.getenv("DB_NAME", "exampledb")
        db_user = os.getenv("DB_USER", "user")
        db_password = os.getenv("DB_PASSWORD", "password")
        db_port = int(os.getenv("DB_PORT", 5432))

    try:
        print(f"Connecting to database at {db_host}:{db_port} with user {db_user}")
        connection = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            dbname=db_name,
            port=int(db_port)
        )
        print("Database connection established.")
        return connection
    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        raise

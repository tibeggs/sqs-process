# sqs-processor

This project is a Python application that connects to an AWS SQS queue, processes messages, and loads the data into an AWS RDS database. It is designed to be run in a Docker container.

## Project Structure

```
sqs-processor
├── src
│   ├── main.py          # Entry point of the application
│   ├── config.py        # Configuration settings for AWS and SQS
│   ├── database
│   │   ├── __init__.py  # Database module initializer
│   │   └── connection.py # Manages connection to AWS RDS
│   ├── sqs
│   │   ├── __init__.py  # SQS module initializer
│   │   └── client.py     # SQS client logic
│   └── models
│       └── __init__.py  # Models module initializer
├── Dockerfile            # Instructions to build the Docker image
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd sqs-processor
   ```

2. **Create a `.env` file:**
   Copy the `.env.example` to `.env` and fill in your AWS credentials and database connection details.

3. **Build the Docker image:**
   ```bash
   docker build -t sqs-processor .
   ```

4. **Run the application:**
   ```bash
   docker run --env-file .env sqs-processor
   ```

## Usage

The application will connect to the specified SQS queue, process incoming messages, and load the data into the configured AWS RDS database. Ensure that your AWS credentials have the necessary permissions to access SQS and RDS.

## License

This project is licensed under the MIT License.
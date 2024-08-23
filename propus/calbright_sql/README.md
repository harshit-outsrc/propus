# Calbright SQL


## Setting Up An Initial Localhost Development

1. First log into your localhost PSQL instance and create a Database
    ```
    -- Create a new user
    CREATE USER calbright WITH PASSWORD '<INSERT_PASSWORD>';
    -- Create database
    CREATE DATABASE calbright_dev WITH OWNER = calbright ENCODING = 'UTF8' CONNECTION LIMIT = -1 IS_TEMPLATE = False;
    -- Create UUID Extension
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    ```
2. If needed, install the [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) by running the following command:
    ```
    curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg";sudo installer -pkg AWSCLIV2.pkg -target /
    ```
3. If needed, set the [AWS Access Key ID and AWS Secret Access Key](https://us-east-1.console.aws.amazon.com/iamv2/home#/security_credentials?section=IAM_credentials) by running the following command:
    ```
    aws configure
    AWS Access Key ID [None]: <YOUR_AWS_ACCESS_KEY_ID>
    AWS Secret Access Key [None]: <YOUR_AWS_SECRET_ACCESS_KEY>
    Default region name [None]: us-west-2
    Default output format [None]: json
    ```
4. Initialize the database by running the following command:
   ```
   export localhost="true" DB="calbright_dev" USER="calbright" PASSWORD="<INSERT_PASSWORD>" env="localhost";python propus/sql/calbright/build_db.py
   ```

## Introducing New Database Changes

Migrations are handled by alembic and additional documentation can be found [here](https://alembic.sqlalchemy.org/en/latest/).
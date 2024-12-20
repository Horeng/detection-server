# Setup & Run Airflow

## Configuring Airflow - by extending the official image

> **CAUTION**
> Ensure that the `.env` file is created and the necessary directories are created.
> Copy the `.env.example` file to `.env` and fill in the necessary values(e.g., start with `YOUR_`).

```bash
# Initialize the airflow server.
docker compose --env-file .env up airflow-init
# If the airflow-init is successful, you can start the airflow server.
docker compose --env-file .env up
# or use below command to run in detached(background) mode
docker compose --env-file .env up -d
# To run the airflow server with flower, use below command
docker compose --env-file .env --profile flower up -d
```

- By default,
    - the airflow server can be accessed at [http://localhost:8080](http://localhost:8080).
        - username: The value of `_AIRFLOW_WWW_USER_USERNAME` in `.env` file.
        - password: The value of `_AIRFLOW_WWW_USER_PASSWORD` in `.env` file.
    - the flower can be accessed at [http://localhost:5555](http://localhost:5555).

> **Note**
> For the convenience, we provide a shortcut for `docker compose` command.
> Please refer to [scripts/shortcuts.sh](../scripts/shortcuts.sh) for more details.

> **Note**
> There exists an another way to configure airflow by customizing the official image.
> Please refer to [Airflow Documentation](https://airflow.apache.org/docs/docker-stack/build.html) for more details.

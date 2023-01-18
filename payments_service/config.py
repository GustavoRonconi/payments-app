from prettyconf import config


class Settings:
    LOG_LEVEL = config("LOG_LEVEL", default="INFO")
    LOGGERS = config("LOGGERS", default="", cast=config.list)

    WAIT_TIME_SECONDS = config("WAIT_TIME_SECONDS", default="5", cast=config.eval)

    AWS_DEFAULT_REGION = config("AWS_DEFAULT_REGION", default="us-east-1")
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="1234")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="1234")
    AWS_ENDPOINT_URL = config("AWS_ENDPOINT_URL", default="http://localhost:4566")
    AWS_USE_SSL = config("AWS_USE_SSL", default=True, cast=config.boolean)
    SNS_DRY_RUN = config("SNS_DRY_RUN", default=False, cast=config.boolean)

    PAYMENTS_API_URL = config("PAYMENTS_API_URL", default="http://localhost:8000/v1")
    TOKEN = config(
        "TOKEN",
        default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc0MDgzMjk1LCJpYXQiOjE2NzQwNzk2OTUsImp0aSI6ImM5YjVhNWIxOTQxZTRmNGRhYTkyNzcyMjliYWEwYzQzIiwidXNlcl9pZCI6MX0.o9BrUpIpv_7Rg8lcYuU1PE401KeDuVwJBSEDWOt3MwM",
    )

    ENVIRONMENT = config("ENVIRONMENT", default="dev")

    SENTRY_DSN = config("SENTRY_DSN", default="")

    PAYMENTS_DEBT_QUEUE = config(
        "PAYMENTS_DEBT_QUEUE", default="csv_file__created__payments_debt"
    )
    CHUNK_SIZE = config("CHUNK_SIZE", default="100", cast=int)


settings = Settings()

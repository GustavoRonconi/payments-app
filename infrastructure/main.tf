# Public Cloud Configuration
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test123"
  secret_key                  = "testabc"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true
  s3_use_path_style           = true
  endpoints {
    s3  = "http://localhost:4566"
    sns = "http://localhost:4566"
    sqs = "http://localhost:4566"
  }
}


resource "aws_s3_bucket" "csv-files" {
  bucket = "csv-files"
}

resource "aws_s3_bucket_acl" "example_bucket_acl" {
  bucket = aws_s3_bucket.csv-files.id
  acl    = "public-read"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.csv-files.id

  topic {
    topic_arn     = aws_sns_topic.csv-file-created.arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = ".csv"
  }
}

resource "aws_sns_topic" "csv-file-created" {
  name = "csv_file__created"

  policy = <<POLICY
{
    "Version":"2012-10-17",
    "Statement":[{
        "Effect": "Allow",
        "Principal": { "Service": "s3.amazonaws.com" },
        "Action": "SNS:Publish",
        "Resource": "arn:aws:sns:*:*:csv_file__created",
        "Condition":{
            "ArnLike":{"aws:SourceArn":"${aws_s3_bucket.csv-files.arn}"}
        }
    }]
}
POLICY
}

resource "aws_sqs_queue" "dead-csv-file-created-payments-debt" {
  name = "dead__csv_file__created__payments_debt"
}

resource "aws_sqs_queue" "csv-file-created-payments-debt" {
  name                      = "csv_file__created__payments_debt"
  delay_seconds             = 10
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dead-csv-file-created-payments-debt.arn
    maxReceiveCount     = 4
  })
}

resource "aws_sns_topic_subscription" "csv-file-created-target" {
  topic_arn = aws_sns_topic.csv-file-created.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.csv-file-created-payments-debt.arn
}

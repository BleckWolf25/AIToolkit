resource "aws_s3_bucket" "b" {
  bucket = "my-bucket"
}

resource "aws_s3_bucket_public_access_block" "b_private" {
  bucket = aws_s3_bucket.b.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
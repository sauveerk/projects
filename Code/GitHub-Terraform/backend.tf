#Configure AWS S3 bucket as remote backend 

terraform {
  backend "s3" {
    bucket         = "terraform-state-backend-xxxxxx"    #Provide S3 bucket
    key            = "ec2-provision/terraform-ec2.tfstate"
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "tfstate-locking-xxxxx"   #Provide DynamoDB table
  }
}
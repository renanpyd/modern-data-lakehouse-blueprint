variable "aws_region" {
  type        = string
  description = "Target cloud deployment infrastructure region."
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Execution tier deployment environment target."
  default     = "production"
}

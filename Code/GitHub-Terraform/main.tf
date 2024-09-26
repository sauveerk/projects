# Creating a security group to restrict/allow inbound connectivity
resource "aws_security_group" "ec2-security-group" {
  name        = var.ec2-security-group-name
  description = "Allow TLS inbound traffic"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # Not recommended to add "0.0.0.0/0" instead we need to be more specific with the IP ranges to allow connectivity from.
  tags = {
    Name = "ec2-sg-inbound"
  }
}


# Creating Ubuntu EC2 instance
resource "aws_instance" "ubuntu-ec2-instance" {
  ami                         = var.ubuntu-ami
  instance_type               = var.ubuntu-instance-type
  vpc_security_group_ids      = [aws_security_group.ec2-security-group.id]
  associate_public_ip_address = true
  tags = {
    Name = "Terraform-VM"
  }
}
I have added few AWS projects here. These are mini versions of real world use cases. Many of these are modular projects which are expanded upon in real production use-cases.

- a) Hybrid DNS - A real world requirement when organization has both cloud and on-prem environment
- b) Instance Stopper - Organizations have some set up to stop non-prod instances over weekend and/or during non-business hours. In mature phases, it is expanded to non-critical production systems also. This is a good FinOps practice.
- c) Transit Gateway - Organization use Transit Gateway to connect their multiple VPCs present in multiple accounts. 
- d) Auto Tagging - A mature tagging practice is a must in any organization. This is helpful in tracking cost and security by assigning responsibilities and holding people accountable. Tagging is first included in deployment stage itself, to avoid leftovers, auto-tagging is also enabled using lambda or step functions.
- e) IaC CI/CD Pipeline - Organizations deploy resources using Infra as Code (IaC), generally using Terraform (the most popular) or Cloudformation (for AWS), using a CI/CD pipeline.
- f) Lamdba, S3, DynamoDB - Along with API Gateway (entrypoint) and Cognito (authorization) these three services are building blocks of serverless applications in AWS. This project though is an example of event driven serverlss architecture.
- g) Step Functions - Step Functions are a great way to orchestrate multiple activities, in this example, before terminating any server, an AMI is created for backup. 
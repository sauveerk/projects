I have added few AWS projects here. These are mini versions of real world use cases. Many of these are modular projects which are expanded upon in real production use cases.

- Static Serverless Website - Static websites can be deployed using AWS S3 buckets and Cloudfront (optional). **Note-** In fact, dynamic websites can also be deployed where S3 holds the static front end and API Gateway and Lambda functions provide dynamic backend. I will do a different projecg to showcase it.
  
  https://github.com/sauveerk/projects/blob/main/Cloudfront-S3-Resume.md
  
-  Hybrid DNS - A real world requirement when organization has both cloud and on-prem environment
  
  https://github.com/sauveerk/projects/blob/main/Hybrid-DNS-AWS-Route53-Resolvers.md 
  
- Transit Gateway - Organizations use Transit Gateway to connect their multiple VPCs present in multiple accounts. 
  
  https://github.com/sauveerk/projects/blob/main/Connecting-VPCs-Using-TransitGateway.md 

- Centralized VPC Endpoints - 

https://github.com/sauveerk/projects/blob/main/Hub-and-Spoke-VPC-Interface-Endpoints.md
  
- Service Catalog - Organizations use Service Catalog to provide self service to end users. End users can quickly deploy only the approved IT services they need, following the constraints set by your organization. Service Catalouge can also be integrated with ITSM tools like Service Now. Users can submit Service Now requests which will trigger creation of the product in AWS.
  
- Instance Stopper - Organizations have some set up to stop non-prod instances over weekend and/or during non-business hours. In mature phases, it is expanded to non-critical production systems also. This is a good FinOps practice.
  
  https://github.com/sauveerk/projects/blob/main/InstanceStopper-LambdaFunction.md
    
- Auto Tagging - A mature tagging practice is a must in any organization. This is helpful in tracking cost and security by assigning responsibilities and holding people accountable. Tagging is first included in deployment stage itself, to avoid leftovers, auto-tagging is also enabled using lambda or step functions.
  
  https://github.com/sauveerk/projects/blob/main/Lambda-EBS-Volume-AutoTagging.md
  
- Lamdba, S3, DynamoDB - Along with API Gateway (entrypoint) and Cognito (authorization) these three services are building blocks of serverless applications in AWS. This project though is an example of event driven serverlss architecture.
  
  https://github.com/sauveerk/projects/blob/main/Lambda-S3-Upload-DynamoDB-Inventory.md
    
- Step Functions - Step Functions are a great way to orchestrate multiple activities, in this example, before terminating any server, an AMI is created for backup. 
  
  https://github.com/sauveerk/projects/blob/main/StepFunctions-EC2.md
  
- IaC CI/CD Pipeline - Organizations deploy resources using Infra as Code (IaC), generally using Terraform (the most popular) or Cloudformation (for AWS), using a CI/CD pipeline.
  
  https://github.com/sauveerk/projects/blob/main/Cloudformation-Iac-CI-CD-Pipeline.md
    
- Kubernetes Deployment - Deploying to an EKS cluster using DevOps and GitOps methods. Explaining difference between DevOps and GitOps methods.
  
  https://github.com/sauveerk/projects/blob/main/Kubernetes-CI-CD-Pipeline.md

  https://github.com/sauveerk/projects/blob/main/Kubernetes-GitOps.md



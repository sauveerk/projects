I have added few AWS projects here. These are mini versions of real world use cases. Many of these are modular projects which are expanded upon in real production use cases.

These projects are grouped into various categories.

## Landing Zone
 
-  **Hybrid DNS** - A real world requirement when organization has both cloud and on-prem environment
  
   https://github.com/sauveerk/projects/blob/main/Hybrid-DNS-AWS-Route53-Resolvers.md 
  
- **Transit Gateway** - Organizations use Transit Gateway to connect multiple VPCs present in multiple accounts. 
  
   https://github.com/sauveerk/projects/blob/main/Connecting-VPCs-Using-TransitGateway.md 

- **Centralized VPC Endpoints** - VPC endpoints are private connections between your VPC and another AWS service without sending traffic over the internet, through a NAT instance, a VPN connection, or AWS Direct Connect. Organizations use hub and spoke design where all the spoke VPCs use an interface VPC endpoint provisioned inside the hub (shared services) VPC. This architecture may help reduce the cost and maintenance for multiple interface VPC endpoints across different VPCs.

   https://github.com/sauveerk/projects/blob/main/Hub-and-Spoke-VPC-Interface-Endpoints.md

- **Access AWS Accounts with Azure Active Directory Federation** - Organisations do not use AWS IAM directly, generally, they use a central identity management system,  for example, an on-premises Active Directory (AD) or the cloud service Microsoft Azure Active Directory (Azure AD). Instead of implementing user lifecycle processes in each environment, it’s easier, more reliable, and more secure to implement them in a central user identity store such as Azure AD.
  
  https://github.com/sauveerk/projects/blob/main/AzureAD-Federation-AWS-Access.md
  
## Resource Provisioning

- **Service Catalog** - Organizations use Service Catalog to provide self service to end users. End users can quickly deploy only the approved IT services they need, following the constraints set by your organization. Service Catalouge can also be integrated with ITSM tools like Service Now. Users can submit Service Now requests which will trigger creation of the product in AWS.
  
  https://github.com/sauveerk/projects/blob/main/Service-Catalog.md

- **IaC CI/CD Pipeline** - Organizations deploy resources using Infra as Code (IaC), generally using Terraform (the most popular) or Cloudformation (for AWS), using a CI/CD pipeline.
  
  https://github.com/sauveerk/projects/blob/main/Cloudformation-Iac-CI-CD-Pipeline.md

## Automation
    
- **Instance Stopper** - Organizations have some set up to stop non-prod instances over weekend and/or during non-business hours. In mature phases, it is expanded to non-critical production systems also. This is a good FinOps practice.
  
  https://github.com/sauveerk/projects/blob/main/InstanceStopper-LambdaFunction.md
    
- **Auto Tagging** - A mature tagging practice is a must in any organization. This is helpful in tracking cost and security by assigning responsibilities and holding people accountable. Tagging is first included in deployment stage itself, to avoid leftovers, auto-tagging is also enabled using lambda or step functions.
  
  https://github.com/sauveerk/projects/blob/main/Lambda-EBS-Volume-AutoTagging.md

- **Step Functions** - Step Functions are a great way to orchestrate multiple activities, in this example, before terminating any server, an AMI is created for backup. 
  
  https://github.com/sauveerk/projects/blob/main/StepFunctions-EC2.md

## Applications & DevOps

- **Static Serverless Website** - Static websites can be deployed using AWS S3 buckets and Cloudfront (optional). 
  
  **Note-** In fact, serverless dynamic websites can also be deployed where S3 holds the static front end and API Gateway and Lambda functions provide dynamic backend. I will do a different project to showcase it.
  
   https://github.com/sauveerk/projects/blob/main/Cloudfront-S3-Resume.md
  
- **Lamdba, S3, DynamoDB** - Along with API Gateway (entrypoint) and Cognito (authorization) these three services are building blocks of serverless applications in AWS. This project though is an example of event driven serverlss architecture.
  
  https://github.com/sauveerk/projects/blob/main/Lambda-S3-Upload-DynamoDB-Inventory.md

    
- **Kubernetes Deployment** - Deploying to an EKS cluster using DevOps and GitOps methods. Explaining difference between DevOps and GitOps methods.
  
  https://github.com/sauveerk/projects/blob/main/Kubernetes-CI-CD-Pipeline.md

  https://github.com/sauveerk/projects/blob/main/Kubernetes-GitOps.md

## Design Patterns

- **Implementing a Fanout Pattern using SNS and SQS in AWS** - The fanout messaging pattern is a common application integration design pattern used to decouple frontend from backend systems. Here, a single message is sent to multiple endpoints. In AWS, this can be efficiently achieved by integrating Amazon SNS and Amazon SQS.

  https://github.com/sauveerk/projects/blob/main/FanoutPattern-SNS-SQS.md



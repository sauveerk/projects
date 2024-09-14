I have added few AWS projects here. These are mini versions of real world use cases. Many of these are modular projects which are expanded upon in real production use cases.

These projects are grouped into various categories.

## Landing Zone
 
- **Transit Gateway** - Organizations generally use Transit Gateway to connect multiple VPCs present in multiple accounts. AWS Transit Gateway provides a hub and spoke design for connecting VPCs and on-premises networks as a fully managed service without requiring you to provision third-party virtual appliances.  
  
   https://github.com/sauveerk/projects/blob/main/Connecting-VPCs-Using-TransitGateway.md 

- **Centralized VPC Endpoints** - VPC endpoints are private connections between your VPC and another AWS service without sending traffic over the internet, through a NAT instance, a VPN connection, or AWS Direct Connect. Organizations use hub and spoke design where all the spoke VPCs use an interface VPC endpoint provisioned inside the hub (shared services) VPC. This architecture may help reduce the cost and maintenance for multiple interface VPC endpoints across different VPCs.

   https://github.com/sauveerk/projects/blob/main/Hub-and-Spoke-VPC-Interface-Endpoints.md

-  **Hybrid DNS** - Many organizations have both on-premises resources and resources in the cloud. DNS name resolution is essential for on-premises and cloud-based resources. For customers with hybrid workloads, which include both on-premises and cloud-based resources, extra steps are necessary to configure DNS to work seamlessly across both environments.
 
   https://github.com/sauveerk/projects/blob/main/Hybrid-DNS-AWS-Route53-Resolvers.md 

- **Access AWS Accounts with Azure Active Directory (Entra) Federation** - Organizations do not use AWS IAM directly, generally, they use a central identity management system, for example, an on-premises Active Directory (AD) or the cloud service Microsoft Azure Active Directory (Azure AD). Instead of implementing user lifecycle processes in each environment, it’s easier, more reliable, and more secure to implement them in a central user identity store such as Azure AD.
  
  https://github.com/sauveerk/projects/blob/main/AzureAD-Federation-AWS-Access.md

- **Centralized Logging** - A key component of enterprise multi-account environments is logging. Centralized logging provides a single point of access to all salient logs generated across accounts and regions, and is critical for auditing, security and compliance. While some customers use the built-in ability to push Amazon CloudWatch Logs directly into Amazon Elasticsearch Service for analysis, others would prefer to move all logs into a centralized Amazon Simple Storage Service (Amazon S3) bucket location for access by several custom and third-party tools or directly sending to third party tools like Splunk via Amazon Data Firehose. 
  
## Resource Provisioning

- **Service Catalog** - Organizations use Service Catalog to provide self-service to end users. End users can quickly deploy only the approved IT services they need, following the constraints set by your organization. Service Catalog can also be integrated with ITSM tools like Service Now. Users can submit Service Now requests which will trigger creation of the product in AWS.
  
  https://github.com/sauveerk/projects/blob/main/Service-Catalog.md

- **IaC CI/CD Pipeline** - Organizations deploy resources using Infra as Code (IaC), generally using Terraform (the most popular) or CloudFormation (for AWS), using a CI/CD pipeline.
  
  https://github.com/sauveerk/projects/blob/main/Cloudformation-Iac-CI-CD-Pipeline.md

## Automation
    
- **Instance Stopper** - Organizations have some set up to stop non-prod instances over weekend and/or during non-business hours. In mature phases, it is expanded to non-critical production systems also. This is a good FinOps practice.
  
  https://github.com/sauveerk/projects/blob/main/InstanceStopper-LambdaFunction.md
    
- **Auto Tagging** - A mature tagging practice is a must in any organization. This is helpful in tracking cost and security by assigning responsibilities and holding people accountable. Tagging is first included in deployment stage itself, to avoid leftovers, auto-tagging is also enabled using lambda or step functions.
  
  https://github.com/sauveerk/projects/blob/main/Lambda-EBS-Volume-AutoTagging.md

- **Step Functions** - Step Functions are a great way to orchestrate multiple activities, in this example, before terminating any server, an AMI is created for backup. 
  
  https://github.com/sauveerk/projects/blob/main/StepFunctions-EC2.md

## Applications & DevOps

- **Static Serverless Website** - Static websites can be deployed using AWS S3 buckets and CloudFront (optional). 
  
  **Note-** In fact, serverless dynamic websites can also be deployed where S3 holds the front end and API Gateway and Lambda functions provide dynamic backend. Javscript calls backend here.
  
   https://github.com/sauveerk/projects/blob/main/Cloudfront-S3-Resume.md
  
- **Lambda, S3, DynamoDB** - Along with API Gateway (entrypoint) and Cognito (authorization), these three services are building blocks of serverless applications in AWS. Though, this project is an example of event driven serverless architecture. 
  
  https://github.com/sauveerk/projects/blob/main/Lambda-S3-Upload-DynamoDB-Inventory.md
    
- **Kubernetes Deployment** - Deploying to an EKS cluster using DevOps and GitOps methods. Explaining difference between DevOps and GitOps methods.
  
  https://github.com/sauveerk/projects/blob/main/Kubernetes-CI-CD-Pipeline.md

  https://github.com/sauveerk/projects/blob/main/Kubernetes-GitOps.md

## Design Patterns

- **Implementing a Fanout Pattern using SNS and SQS in AWS** - The fanout messaging pattern is a common application integration design pattern used to decouple frontend from backend systems. Here, a single message is sent to multiple endpoints. In AWS, this can be efficiently achieved by integrating Amazon SNS and Amazon SQS.

  https://github.com/sauveerk/projects/blob/main/FanoutPattern-SNS-SQS.md



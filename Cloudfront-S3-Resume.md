# Deploying an AWS S3 Static Website and Putting it Behind CloudFront

- I have created an html file for my resume. Through below steps, I have configured my resume as a S3 static website. 

- S3 static website does not support https, so to make my website secure, I have put it behind a cloudfront distribution. 

- Instead of default domain name provided by AWS, I have configured a custom domain in Route 53. 

- AWS services used - S3, Cloudfront, ACM, Route 53.

![alt text](Images/cf-custom-website.png)

## Step 1: Create an S3 Bucket

- Go to the AWS Management Console and navigate to the S3 service.
- Click on "Create bucket" and follow the prompts to create a new bucket.
- Bucket name can be anything unique. But, if you want to use custom domain, ensure that the bucket name matches your domain name (e.g., sauveer-resume.skcarchitect.org in my case).
  
## Step 2: Upload Your Website Files to the S3 Bucket

- Select your newly created bucket and click on the "Upload" button.
- Upload all your static website files (HTML, CSS, JavaScript, images, etc.) to the bucket.

![alt text](Images/image.png)

## Step 3: Enable Static Website Hosting

- In the bucket properties, navigate to the "Static website hosting" section.
- Select "Use this bucket to host a website" and specify the index document (e.g., index.html).
- Note down the endpoint URL provided (e.g., http://your-bucket-name.s3-website-your-region.amazonaws.com).

![alt text](Images/image-1.png)

![alt text](Images/image-2.png)

## Step 4: Making bucket public

- By default, Amazon S3 blocks public access to your account and buckets. If you want to use a bucket to host a static website, you can use these steps to edit your block public access settings.
- Choose the name of the bucket that you have configured as a static website. Choose Permissions.
- Under Block public access (bucket settings), choose Edit. Clear Block all public access, and choose Save changes.
  
  ![alt text](Images/s3-bpa.png)

- Amazon S3 turns off Block Public Access settings for your bucket. To create a public, static website, you might also have to edit the Block Public Access settings for your account before adding a bucket policy. If account settings for Block Public Access are currently turned on, you see a note under Block public access (bucket settings).
- Finally, add a bucket policy that makes it public. Choose Permissions. Under Bucket Policy, choose Edit. To grant public read access for your website, copy the following bucket policy, and paste it in the Bucket policy editor.
  
 ![alt text](Images/s3-bucketpolicy.png)

- My website is ready now, it can be accessed using bucket website endpoint given under properties. 

![alt text](Images/website-default.png)

- For using a more specific url, I need to create DNS record. I own a domain and I have a public hosted zone in Route 53. I have created an alias to point to s3 static website.

![alt text](Images/Route53-1.png)

![alt text](Images/Route53-2.png)

- Now, I can access my website using custom domain. But, this is http website and hence not secure. To make a S3 static website accessible via https, we need to put it behind a cloudfront distribution. 

![alt text](Images/website-custom.png)

## Step 5: Create a TLS Certificate in ACM

- Go to ACM. You have to select the AWS North Virginia region(US-East-1). As CloudFront recognizes only this region as it's ACM certificates. 
- Reques a certificate. Choose public certificate.

![alt text](Images/ACM-1.png)

- Provide your Domain names, select a Validation method rest all are fine click on request.
  
  ![alt text](Images/ACM-2.png)

- Once you click request, you need to add the given record in Route 53 by clicking on Create records in Route 53.

![alt text](Images/ACM-3.png)

- After some time, certificate will be come available.

![alt text](Images/ACM-4.png)

## Step 6: Create a CloudFront Distribution

- Go to the CloudFront service in the AWS Management Console.
- Click on "Create Distribution". Select your s3 bucket in origin domain.

![alt text](Images/cf-1.png)

- In Viewer protocol policy select to Redirect HTTP to HTTPS.

![alt text](Images/cf-2.png)

- Add custom SSL certificate.

![alt text](Images/cf-3.png)

- Select Web Application Firewall (WAF). You can select as per your requirment.

![alt text](Images/cf-4.png)

- Mention Default root object and Click on Create distribution.

![alt text](Images/cf-5.png)

- After distribution is created, you can access the website using distribution domain name.

![alt text](Images/cf-6.png)

![alt text](Images/cf-default-website.png)

## Step 7: Update DNS Records

- Go to your DNS management console (e.g., Route 53) and update your DNS records.
- Create a new alias record pointing to your CloudFront distribution domain name.

![alt text](Images/R53-cf.png)

- Wait for DNS changes to propagate.
- Website is available now using https.

![alt text](Images/cf-custom-website.png)

- Congratulations! Your AWS S3 static website is now deployed and served through CloudFront.




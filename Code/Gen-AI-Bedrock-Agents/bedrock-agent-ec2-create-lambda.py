import json
import boto3
import botocore.exceptions
import time
import traceback  # Added import for traceback

def lambda_handler(event, context):
    """
    Lambda function to create an EC2 instance based on provided region and instance type,
    and return its ID and public IP. Defaults to ap-south-1 if region parameter is not provided.

    Args:
        event (dict): The event dict from the Bedrock agent.
                      Expected structure includes 'actionGroup', 'function',
                      'sessionAttributes', 'promptSessionAttributes', and 'parameters'.
        context (object): Lambda context object.

    Returns:
        dict: A dictionary formatted for Bedrock agent response,
              containing the new instance's ID and public IP.
    """
    # Default region - Changed to ap-south-1
    region = 'ap-south-1'
    instance_type = None
    ami_id = 'ami-0f1dcc636b69a6438' # *** IMPORTANT: REPLACE with a valid AMI ID for your target region and OS ***
                                    # You can find AMI IDs in the EC2 console or using AWS CLI/SDK (e.g., describe-images)
                                    # Consider using a Systems Manager Parameter Store to store the latest AMI ID dynamically.

    # Ensure Lambda role has ec2:RunInstances, ec2:DescribeInstances permissions.
    # If assigning a Public IP requires modifying the network interface,
    # ec2:CreateNetworkInterface, ec2:AttachNetworkInterface might be needed depending on your VPC config.
    # If the security group needs to be created or modified, relevant ec2 permissions are needed.

    print("Received Event: ", json.dumps(event, indent=2))

    try:
        # --- Extract details from event ---
        action_group = event.get('actionGroup', '')
        invoked_function = event.get('function', '')
        session_attributes = event.get('sessionAttributes', {})
        prompt_session_attributes = event.get('promptSessionAttributes', {})
        parameters = event.get('parameters', []) # Parameters are passed in a list

        # Extract region and instance-type from the parameters list
        # If region is found in parameters, it will override the default
        for param in parameters:
            if param.get('name') == 'region':
                region = param.get('value')
            elif param.get('name') == 'instance-type':
                instance_type = param.get('value')

        if not instance_type: # Region now has a default, so only check instance-type
            raise ValueError("Missing required parameter: 'instance-type'")

        # Initialize EC2 client with the determined region
        ec2 = boto3.client('ec2', region_name=region)

        # --- Core Logic: Create EC2 Instance ---
        print(f"Attempting to create EC2 instance in region {region} with type {instance_type} using AMI ID {ami_id}")

        # --- IMPORTANT SECURITY CONSIDERATIONS ---
        # The following run_instances call uses minimal parameters.
        # For production, you MUST specify:
        # 1. SecurityGroupIds or SecurityGroups: Control network access.
        # 2. SubnetId: Specify the subnet to launch into (determines public IP assignment, availability zone).
        # 3. KeyName: For SSH access (optional but common).
        # 4. IamInstanceProfile: Assign an IAM role to the instance for AWS service access.
        # 5. UserData: To run bootstrap scripts on launch.
        # 6. TagSpecifications: To tag your instances for identification and cost allocation.
        # -----------------------------------------

        run_instances_response = ec2.run_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            # Add SecurityGroupIds, SubnetId, KeyName, etc. here as needed
        )

        new_instance = run_instances_response['Instances'][0]
        new_instance_id = new_instance['InstanceId']
        print(f"Launched instance with ID: {new_instance_id}. Waiting for it to enter 'running' state.")

        # Wait for the instance to be running
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[new_instance_id],
                    WaiterConfig={'Delay': 5, 'MaxAttempts': 20}) # Wait up to 100 seconds

        print(f"Instance {new_instance_id} is now running. Describing instance to get IP.")

        # Describe the instance to get its public IP address
        describe_response = ec2.describe_instances(InstanceIds=[new_instance_id])
        running_instance = describe_response['Reservations'][0]['Instances'][0]
        public_ip_address = running_instance.get('PublicIpAddress', 'No public IP assigned') # Handle case where no public IP

        print(f"Instance {new_instance_id} details: Public IP: {public_ip_address}")

        # --- End Core Logic ---

        # --- Prepare the Payload ---
        # This structure MUST match how you describe the function's
        # return value in the Bedrock console's "Function Details" section.
        payload = {
            "instanceId": new_instance_id,
            "publicIpAddress": public_ip_address,
            "region": region # Optionally include the region in the response
        }
        print("Payload Dictionary:", payload)

        # Stringify the payload - Bedrock expects the body as a string
        stringified_payload_body = json.dumps(payload)
        print("Stringified Payload Body:", stringified_payload_body)
        # --- End Prepare the Payload ---

        # --- Construct the innermost responseBody map ---
        # Use 'TEXT' as required by Bedrock for functionContent.
        content_type_key = 'TEXT'
        response_body_map = {
            content_type_key: {
                'body': stringified_payload_body
            }
        }
        # --- End Construct the innermost responseBody map ---

        # --- Construct the functionResponse object ---
        function_response_part = {
             'responseBody': response_body_map
        }
        # --- End Construct the functionResponse object ---

        # --- Assemble the main 'response' object ---
        # Use 'function' key matching the event, and nest 'functionResponse'
        agent_response_part = {
            'actionGroup': action_group,
            'function': invoked_function,
            'functionResponse': function_response_part
        }
        # --- End Assemble the main 'response' object ---

        # --- Build the final return object ---
        bedrock_response = {
            'messageVersion': '1.0',
            'response': agent_response_part,
            'sessionAttributes': session_attributes,
            'promptSessionAttributes': prompt_session_attributes
        }
        # --- End Build the final return object ---

        print("Returning Bedrock Response: ", json.dumps(bedrock_response, indent=2))
        return bedrock_response

    except botocore.exceptions.ClientError as e:
        # Handle AWS API errors (e.g., InvalidInstanceType, UnauthorizedOperation)
        print(f"AWS API Error: {e}")
        traceback.print_exc()  # Print full traceback
        error_message = f"Failed to create EC2 instance due to AWS API error: {e.response.get('Error', {}).get('Message', str(e))}"
        error_payload = {'errorMessage': error_message}

        # Determine the key ('function' or 'apiPath') based on what was likely in the event
        invoked_identifier = event.get('function') or event.get('apiPath', 'N/A')
        response_key_type = 'function' if event.get('function') else 'apiPath'

        error_body_map = {
            'TEXT': { # Use 'TEXT' for error messages
                'body': json.dumps(error_payload) # Stringify the error payload
            }
        }

        error_function_response = {
            'responseState': 'FAILURE', # Indicate failure
            'responseBody': error_body_map
        }

        error_agent_response = {
            'actionGroup': event.get('actionGroup', 'N/A'),
            response_key_type: invoked_identifier,
            'functionResponse': error_function_response
        }

        bedrock_error_response = {
            'messageVersion': '1.0',
            'response': error_agent_response,
            'sessionAttributes': event.get('sessionAttributes', {}),
            'promptSessionAttributes': event.get('promptSessionAttributes', {})
        }

        print("Returning Bedrock Error Response: ", json.dumps(bedrock_error_response, indent=2))
        return bedrock_error_response

    except ValueError as e:
         # Handle missing required parameters
        print(f"Parameter Error: {e}")
        error_message = f"Missing required input: {str(e)}. Please provide the instance type." # Adjusted message since region is defaulted
        error_payload = {'errorMessage': error_message}

        invoked_identifier = event.get('function') or event.get('apiPath', 'N/A')
        response_key_type = 'function' if event.get('function') else 'apiPath'

        error_body_map = {
            'TEXT': {
                'body': json.dumps(error_payload)
            }
        }

        error_function_response = {
            'responseState': 'REPROMPT', # Use REPROMPT to ask the user for missing info
            'responseBody': error_body_map
        }

        error_agent_response = {
            'actionGroup': event.get('actionGroup', 'N/A'),
            response_key_type: invoked_identifier,
            'functionResponse': error_function_response
        }

        bedrock_error_response = {
            'messageVersion': '1.0',
            'response': error_agent_response,
            'sessionAttributes': session_attributes, # Pass back existing session attributes
            'promptSessionAttributes': prompt_session_attributes # Pass back existing prompt session attributes
        }
        print("Returning Bedrock Error Response (Reprompt): ", json.dumps(bedrock_error_response, indent=2))
        return bedrock_error_response


    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {str(e)}")
        traceback.print_exc()  # Print full traceback
        error_message = f"An unexpected error occurred: {str(e)}"
        error_payload = {'errorMessage': error_message}

        invoked_identifier = event.get('function') or event.get('apiPath', 'N/A')
        response_key_type = 'function' if event.get('function') else 'apiPath'

        error_body_map = {
            'TEXT': {
                'body': json.dumps(error_payload)
            }
        }

        error_function_response = {
            'responseState': 'FAILURE',
            'responseBody': error_body_map
        }

        error_agent_response = {
            'actionGroup': event.get('actionGroup', 'N/A'),
            response_key_type: invoked_identifier,
            'functionResponse': error_function_response
        }

        bedrock_error_response = {
            'messageVersion': '1.0',
            'response': error_agent_response,
            'sessionAttributes': event.get('sessionAttributes', {}),
            'promptSessionAttributes': event.get('promptSessionAttributes', {})
        }

        print("Returning Bedrock Error Response: ", json.dumps(bedrock_error_response, indent=2))
        return bedrock_error_response
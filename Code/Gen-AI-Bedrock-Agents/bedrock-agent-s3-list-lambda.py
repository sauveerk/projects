import json
import boto3
import botocore.exceptions
import traceback  # Added import for traceback

def lambda_handler(event, context):
    """
    Lambda function to list S3 buckets for a Bedrock agent action group.

    Args:
        event (dict): The event dict from the Bedrock agent.
                      Expected structure includes 'actionGroup', 'function',
                      'sessionAttributes', 'promptSessionAttributes'.
        context (object): Lambda context object.

    Returns:
        dict: A dictionary formatted for Bedrock agent response,
              containing the list of S3 bucket names.
    """
    s3 = boto3.client('s3')
    # IMPORTANT: Ensure this Lambda function's IAM role has the
    # 's3:ListAllMyBuckets' permission.

    print("Received Event: ", json.dumps(event, indent=2))

    try:
        # --- Extract details from event ---
        # For "Function Details" method, expect 'function' key from the event
        action_group = event.get('actionGroup', '')
        invoked_function = event.get('function', '') # Use the 'function' key from the event
        session_attributes = event.get('sessionAttributes', {})
        prompt_session_attributes = event.get('promptSessionAttributes', {})

        # --- Core Logic: List S3 Buckets ---
        bucket_names = []
        try:
            response = s3.list_buckets()
            if 'Buckets' in response:
                for bucket in response['Buckets']:
                    bucket_names.append(bucket['Name'])
        except botocore.exceptions.ClientError as e:
             # Handle specific S3 permissions or API errors
             print(f"S3 ClientError: {e}")
             traceback.print_exc()  # Print full traceback
             # Re-raise the exception to be caught by the outer handler
             raise e
        except Exception as e:
            # Handle any other exceptions during S3 listing
            print(f"Error listing S3 buckets: {e}")
            traceback.print_exc()  # Print full traceback
            raise e

        # --- End Core Logic ---

        # --- Prepare the Payload ---
        # This structure should implicitly match how you described the function's
        # return value in the Bedrock console's "Function Details" section
        # (e.g., if you defined a response property named 'bucketList' as a list
        # of strings).
        payload = {
            "bucketNames": bucket_names,
            "count": len(bucket_names)
        }
        print("Payload Dictionary:", payload)

        # Stringify the payload - Bedrock expects the body as a string
        # The content type must match what you defined in the Bedrock action group
        # schema for the response body.
        stringified_payload_body = json.dumps(payload)
        print("Stringified Payload Body:", stringified_payload_body)
        # --- End Prepare the Payload ---

        # --- Construct the innermost responseBody map ---
        # This MUST use the 'TEXT' key for text content, as required by Bedrock
        # for the 'functionContent' type.
        content_type_key = 'TEXT'
        response_body_map = {
            content_type_key: {
                'body': stringified_payload_body
            }
        }
        # --- End Construct the innermost responseBody map ---

        # --- Construct the functionResponse object ---
        # This contains the responseBody map and optionally responseState.
        function_response_part = {
            #'responseState': 'SUCCESS', # Indicate successful execution
            'responseBody': response_body_map
        }
        # --- End Construct the functionResponse object ---

        # --- Assemble the main 'response' object ---
        # Use 'function' key matching the event, and nest 'functionResponse'
        agent_response_part = {
            'actionGroup': action_group,
            'function': invoked_function, # Mirror the 'function' key from the event
            'functionResponse': function_response_part # Embed the nested structure
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

    except Exception as e:
        print(f"Error processing event: {str(e)}")
        traceback.print_exc()  # Print full traceback

        # --- Construct error response ---
        # Format the error response following the structure as best as possible
        error_message = f"An error occurred while listing S3 buckets: {str(e)}"
        error_payload = {'errorMessage': error_message}

        # Determine the key ('function' or 'apiPath') based on what was likely in the event
        invoked_identifier = event.get('function') or event.get('apiPath', 'N/A')
        response_key_type = 'function' if event.get('function') else 'apiPath'


        # The error response body can also be TEXT, particularly for simple error messages
        error_body_map = {
            'TEXT': { # Use 'TEXT' for error messages too
                'body': json.dumps(error_payload) # Stringify the error payload
            }
        }

        error_function_response = {
            'responseState': 'FAILURE', # Indicate failure
            'responseBody': error_body_map
        }

        error_agent_response = {
            'actionGroup': event.get('actionGroup', 'N/A'),
            response_key_type: invoked_identifier, # Use the identified key
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
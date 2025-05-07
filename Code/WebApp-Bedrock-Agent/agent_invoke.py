import boto3
import json
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any
import uuid

def invoke_bedrock_agent(prompt: str) -> Optional[Dict[Any, Any]]:
    """
    Invoke a Bedrock agent with the given prompt.
    
    Args:
        prompt (str): The prompt to send to the agent
        
    Returns:
        Optional[Dict]: The agent's response or None if an error occurs
    """
    try:
        bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')
    except Exception as e:
        print(f"Error creating Bedrock client: {str(e)}")
        return None
    
    if not prompt or not isinstance(prompt, str):
        print("Error: Prompt must be a non-empty string")
        return None
        
    try:
        session_id = str(uuid.uuid4())
        
        response = bedrock_agent_runtime.invoke_agent(
            agentId='VGGUJUPSEC',
            agentAliasId='RAZCHX6EDM',
            sessionId=session_id,
            inputText=prompt
        )
        
        # Handle the event stream response
        full_response = ""
        for event in response['completion']:
            if 'chunk' in event:
                chunk_data = event['chunk']['bytes'].decode('utf-8')
                full_response += chunk_data
        
        # Parse the complete response if needed
        if full_response:
            try:
                return json.loads(full_response)
            except json.JSONDecodeError:
                # If response is not JSON, return as plain text
                return {"response": full_response}
        else:
            print("Error: Empty response from Bedrock Agent")
            return None
            
    except ClientError as e:
        print(f"AWS API Error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def main():
    prompt = input("Enter your prompt: ")
    response = invoke_bedrock_agent(prompt)

    if response:
        print("Agent Response:")
        if isinstance(response, dict):
            print(json.dumps(response, indent=2))
        else:
            print(response)
    else:
        print("Failed to get response from agent")

if __name__ == "__main__":
    main()

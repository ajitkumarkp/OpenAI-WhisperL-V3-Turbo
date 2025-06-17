import json
import boto3
import base64
import os

# Option 1: If you want to use Amazon Bedrock
def transcribe_with_bedrock(audio_file_path):
    # Initialize Bedrock Runtime client
    bedrock_runtime = boto3.client("bedrock-runtime")
    
    # Read audio file
    with open(audio_file_path, "rb") as audio_file:
        audio_data = audio_file.read()
        hex_audio = audio_data.hex()

    request_body = json.dumps({
        "audio_input": hex_audio,
        "top_p": 0.9,
        "language": "english",
        "task": "transcribe",
    })
   
    endpoint_arn = "arn:aws:sagemaker:us-east-1:640588260050:endpoint/whisper-bedrock-endpoint"

    response = bedrock_runtime.invoke_model(
        modelId=endpoint_arn,  # Replace with your desired Bedrock model
        body=request_body,
        # contentType="application/json",
        # accept="application/json"
    )
    
    # Parse response
    response_body = json.loads(response.get('body').read())
    return response_body

# Option 2: If you want to use SageMaker endpoint (fixing your original code)
def transcribe_with_sagemaker(audio_file_path, endpoint_name):
    # Initialize SageMaker Runtime client
    sagemaker_runtime = boto3.client('runtime.sagemaker')
    
    # Read audio file
    with open(audio_file_path, "rb") as file:
        audio_data = file.read()
    
    # Invoke SageMaker endpoint directly with audio data for WAV format
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="audio/wav",
        Body=audio_data
    )
    
    # Parse response
    response_body = json.loads(response['Body'].read())
    return response_body.get('text')

# Example usage
if __name__ == "__main__":
    # Path to your audio file
    # audio_file = "test_recordings_for_aws_eval/Cholesterol-drugs.wav"
    
    audio_file = os.path.join("audio_samples", "sample1-mp3.mp3") 
    
    # For SageMaker endpoint
    endpoint_name = "whisper-bedrock-endpoint"
        
    try:
        # Choose which method to use
        # Option 1: Bedrock
        result = transcribe_with_bedrock(audio_file)
        print(f"Bedrock transcription: {result}")
        
        # Option 2: SageMaker
        # result = transcribe_with_sagemaker(audio_file, endpoint_name)
        # print(f"SageMaker transcription: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
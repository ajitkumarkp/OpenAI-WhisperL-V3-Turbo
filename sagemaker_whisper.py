import boto3
import json
import os

def transcribe_audio(audio_file_path):
    """
    Transcribe audio using Whisper Large v3 Turbo model via SageMaker endpoint
    
    Args:
        audio_file_path: Path to the audio file to transcribe
    
    Returns:
        Transcription result
    """
    # Initialize SageMaker runtime client
    sagemaker_runtime = boto3.client(
        service_name='sagemaker-runtime',
        region_name='us-east-1'
    )
    
    # Read the audio file
    with open(audio_file_path, 'rb') as audio_file:
        audio_data = audio_file.read()
    
    # Determine content type based on file extension
    file_ext = os.path.splitext(audio_file_path)[1].lower()
    content_type = "audio/wav" if file_ext == ".wav" else "audio/mp3"
    
    # Invoke the endpoint
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName="whisper-bedrock-endpoint",
        ContentType=content_type,
        Body=audio_data
    )
    
    # Parse and return the response
    response_body = json.loads(response['Body'].read().decode('utf-8'))
    return response_body

if __name__ == "__main__":
    # Path to your audio file 
    audio_file = os.path.join("audio_samples", "sample1-mp3.mp3")  # Example MP3 file
    # this file is around 4.5MB
        
    print(f"Transcribing audio file: {audio_file}")
    result = transcribe_audio(audio_file)
    
    # Print the transcription result
    print("\nTranscription Result:")
    print(result)  # Print the entire result
import argparse
import os
from datetime import datetime
from openai import AzureOpenAI

def validate_environment():
    """Validate required environment variables exist"""
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            "Please set these variables before running:\n"
            "1. AZURE_OPENAI_API_KEY - Your Azure OpenAI API key\n"
            "2. AZURE_OPENAI_ENDPOINT - Your endpoint URL (e.g. https://resource.openai.azure.com)"
        )

def transcribe_audio(input_path, output_dir=None, model="whisper"):
    """
    Transcribe audio files using Azure OpenAI Whisper
    
    Args:
        input_path (str): Path to audio file (MP3, WAV, M4A, etc.)
        output_dir (str): Output directory for transcripts
        model (str): Deployment name of your Whisper model in Azure
    
    Raises:
        EnvironmentError: If required env vars are missing
        FileNotFoundError: If input file doesn't exist
        Exception: For API/transcription errors
    """
    # Validate environment first
    validate_environment()

    # Verify file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Audio file not found: {input_path}")

    try:
        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") # type: ignore
        )

        print(f"Transcribing {input_path} using Azure OpenAI Whisper...")

        with open(input_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model=model
            )
            transcript = transcription.text

        # Prepare output path
        if output_dir is None:
            output_dir = os.path.dirname(input_path)
        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"{base_name}_transcript_azureopenai_{timestamp}.txt")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        print(f"Success! Transcript saved to: {output_path}")
        return output_path

    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio using Azure OpenAI Whisper",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_path", help="Path to audio file")
    parser.add_argument("--output_dir", help="Output directory", default="transcripts")
    parser.add_argument("--model", help="Azure deployment name", default="whisper")
    
    args = parser.parse_args()
    
    try:
        transcribe_audio(args.input_path, args.output_dir, args.model)
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("\nTroubleshooting tips:")
        print("- Verify environment variables are set")
        print("- Check your Azure OpenAI resource is active")
        print("- Ensure your deployment name is correct")
        print("- Confirm file is <25MB and in supported format")
        exit(1)

if __name__ == "__main__":
    main()

 # Example Usage: python transcribe-azure.py ./audio/20240107_true_happiness.mp3 --output_dir ./transcripts --model whisper
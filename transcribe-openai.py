import argparse
import os
from datetime import datetime
from openai import OpenAI

def transcribe_mp3(input_path, output_dir=None, model_size="whisper-1"):
    """
    Transcribe an MP3 file using OpenAI's Whisper API.
    
    [Documentation: https://platform.openai.com/docs/guides/speech-to-text]
    whisper-1 (original)	** 0.006/min (0.36/hr)	General-purpose, cost-effective	Same as the open-source Whisper model
    gpt-4o-mini (experimental)	** 0.015/min (0.90/hr)	Better accuracy than whisper-1	Optimized for speed & moderate accuracy 
    gpt-4o (experimental)	** 0.03/min (1.80/hr)	Highest accuracy (GPT-4o-level)	Best for complex audio (accents, jargon, noisy environments) 
    
    [Estimating the approximate expense for processing 14,400 minutes (equivalent to 480 sessions of 30-minute audio).]    
    Total cost for whisper-1: $86.00
    Total cost for gpt-4o-mini: $216.00
    Total cost for gpt-4o: $432.00

    Args:
        input_path (str): Path to the MP3 file
        output_dir (str, optional): Directory to save the transcription. Defaults to same directory as input.
        model_size (str, optional): "whisper-1" is the most affordable model.
    """

    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Initialize the OpenAI client
    # Automatically loads API key from `OPENAI_API_KEY` env var
    client = OpenAI()
    
    # Transcribe the audio using OpenAI's API
    print(f"Transcribing {input_path} using OpenAI Whisper API...")
    
    try:
        with open(input_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                file=audio_file,
                model=model_size,
                response_format="text"  # You can also use "json", "srt", "vtt" etc.
            )
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {e}")
    
    # Prepare output file path
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    else:
        os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist
    
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"{base_name}_transcription_openai_{timestamp}.txt")
    
    # Save the transcription
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    
    print(f"Transcription saved to: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Transcribe MP3 files using OpenAI's Whisper API")
    parser.add_argument("input_path", help="Path to the MP3 file to transcribe")
    parser.add_argument("--output_dir", help="Directory to save the transcription file", default="transcripts")
    parser.add_argument("--model", help="Whisper model (only whisper-1 is available via API)", default="whisper-1")
    
    args = parser.parse_args()
    
    try:
        transcribe_mp3(args.input_path, args.output_dir, args.model)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

 # Example Usage: python transcribe.py ./audio/20240107_true_happiness.mp3 --output_dir ./transcripts --model whisper-1
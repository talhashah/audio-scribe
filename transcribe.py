import whisper
import argparse
import os
from datetime import datetime

def transcribe_mp3(input_path, output_dir=None, model_size="base"):
    """
    Transcribe an MP3 file using Whisper.
    
    Args:
        input_path (str): Path to the MP3 file
        output_dir (str, optional): Directory to save the transcription. Defaults to same directory as input.
        model_size (str, optional): Whisper model size (tiny, base, small, medium, large). Defaults to "base".
    """
    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Validate model size
    valid_models = ["tiny", "base", "small", "medium", "large"]
    if model_size not in valid_models:
        raise ValueError(f"Invalid model size. Choose from: {', '.join(valid_models)}")
    
    # Load the Whisper model
    print(f"Loading Whisper {model_size} model...")
    model = whisper.load_model(model_size)
    
    # Transcribe the audio
    print(f"Transcribing {input_path}...")
    result = model.transcribe(input_path, verbose=True) # Set verbose=True to see detailed output
    
    # Prepare output file path
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"{base_name}_transcription_{timestamp}.txt")
    
    # Save the transcription
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(result["text"]))
    
    print(f"Transcription saved to: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Transcribe MP3 files using Whisper")
    parser.add_argument("input_path", help="Path to the MP3 file to transcribe")
    parser.add_argument("--output_dir", help="Directory to save the transcription file", default="transcripts")
    parser.add_argument("--model", help="Whisper model size (tiny, base, small, medium, large)", default="base")
    
    args = parser.parse_args()
    
    try:
        transcribe_mp3(args.input_path, args.output_dir, args.model)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

 # Example Usage: python transcribe.py ./audio/20240107_true_happiness.mp3 --output_dir ./transcripts --model base
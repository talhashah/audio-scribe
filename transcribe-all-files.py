import whisper
import argparse
import os
from datetime import datetime

# Supported audio file extensions
SUPPORTED_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.mp4']
VALID_MODELS = ["tiny", "base", "small", "medium", "large"]

def transcribe_audio_file(file_path, output_dir="transcripts", model_size="base"):
    """
    Transcribe a single audio file using Whisper.
    
    Args:
        file_path (str): Path to the audio file
        output_dir (str): Directory to save the transcription
        model_size (str): Whisper model size
    """
    try:
        # Check if input file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
    
        # Validate model size
        if model_size not in VALID_MODELS:
            raise ValueError(f"Invalid model size. Choose from: {', '.join(VALID_MODELS)}")
        
        print(f"\nProcessing: {os.path.basename(file_path)}")
        
        # Load the Whisper model
        model = whisper.load_model(model_size)
        
        # Transcribe the audio
        result = model.transcribe(file_path)
        
        # Prepare output file path
        if output_dir is None:
            output_dir = os.path.dirname(file_path)
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"{base_name}_transcription_{timestamp}.txt")
        
        # Save the transcription
        with open(output_path, mode="w", encoding="utf-8") as f:
            f.write(str(result["text"]))
        
        print(f"Successfully transcribed. Output saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error processing {os.path.basename(file_path)}: {str(e)}")
        return None

def process_audio_folder(folder_path="audio", output_dir="transcripts", model_size="base"):
    """
    Process all audio files in a folder.
    
    Args:
        folder_path (str): Path to the folder containing audio files
        output_dir (str): Directory to save transcriptions
        model_size (str): Whisper model size
    """
    # Verify the folder exists
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    # Create output directory if it doesn't exist
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get all files in the folder
    files = [f for f in os.listdir(folder_path) 
             if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS]
    
    if not files:
        print(f"No supported audio files found in {folder_path}")
        return
    
    print(f"\nFound {len(files)} audio files to process in {folder_path}")
    
    # Process each file
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        transcribe_audio_file(file_path, output_dir, model_size)

def main():
    parser = argparse.ArgumentParser(description="Transcribe all audio files in a folder using Whisper")
    parser.add_argument("--folder_path", help="Path to the folder containing audio files", default="audio")
    parser.add_argument("--output_dir", help="Directory to save the transcription files", default="transcripts")
    parser.add_argument("--model", help="Whisper model size (tiny, base, small, medium, large)", default="base")
    
    args = parser.parse_args()
    
    try:
        process_audio_folder(args.folder_path, args.output_dir, args.model)
        print("\nAll files processed.")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()

# Example Usage: python transcribe_all_files.py --folder_path ./audio --output_dir ./transcripts --model base
# 🎤 Audio Transcription Toolkit

**Four Python scripts for transcribing audio using different approaches - choose between local or cloud processing.**

## 📋 Features

- **Local Whisper** (CPU/GPU): Free, offline transcription
- **OpenAI API** (Cloud): Pay-per-use with multiple model options
- **Azure OpenAI** (Cloud): Enterprise-grade Whisper API
- **Batch Processing**: Transcribe all files in a folder
- Supports: MP3, WAV, M4A, FLAC, OGG, AAC, MP4

---

## ⚙️ Setup Instructions

### 1. **Install Python 3.9+ (Required for Local Whisper)**

```bash
sudo apt update && sudo apt install python3.9 python3-pip  # Ubuntu/Debian
```

### 2. **Install Dependencies**

```bash
pip install openai python-dotenv whisper
```

### 3. **API Key Configuration**

#### **For OpenAI API Users**

```bash
# Temporary (session only)
export OPENAI_API_KEY="sk-your-key-here"

# Permanent (add to ~/.bashrc)
echo 'export OPENAI_API_KEY="sk-your-key-here"' >> ~/.bashrc && source ~/.bashrc
```

#### **For Azure OpenAI Users**

```bash
# Required environment variables
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
```

---

## 📂 Script Comparison

| Script                    | Description                  | Key Requirement   |
| ------------------------- | ---------------------------- | ----------------- |
| `transcribe.py`           | Local Whisper (single file)  | Python 3.9+       |
| `transcribe_all_files.py` | Local Whisper (batch folder) | Python 3.9+       |
| `transcribe_openai.py`    | Cloud Whisper (OpenAI API)   | OpenAI API Key    |
| `transcribe_azure.py`     | Enterprise Whisper (Azure)   | Azure Credentials |

---

## 🚀 Usage Examples

### 1. **Local Whisper (Single File)**

```bash
python transcribe.py audio/speech.mp3 --output_dir ./results --model medium
```

### 2. **Local Whisper (Batch Folder)**

```bash
python transcribe_all_files.py --folder_path ./audio --output_dir ./results --model large
```

### 3. **OpenAI API (Cloud)**

```bash
python transcribe_openai.py audio/speech.mp3 --model whisper-1
```

### 4. **Azure OpenAI (Enterprise)**

```bash
python transcribe_azure.py audio/speech.mp3 --model whisper-deployment-name
```

---

## ⚡ Performance Notes

### **Local Whisper Models**

| Model  | Speed      | VRAM Usage | Quality |
| ------ | ---------- | ---------- | ------- |
| tiny   | ⚡ Fastest | ~1GB       | Low     |
| base   | Fast       | ~1GB       | Medium  |
| small  | Medium     | ~2GB       | Good    |
| medium | Slow       | ~5GB       | Better  |
| large  | 🐢 Slowest | ~10GB      | Best    |

### **Cloud Services Comparison**

| Service      | Model Options             | Cost/Min | Best For                 |
| ------------ | ------------------------- | -------- | ------------------------ |
| OpenAI API   | whisper-1                 | $0.006   | General use              |
|              | gpt-4o-mini-transcribe    | $0.015   | Better accuracy          |
|              | gpt-4o-transcribe         | $0.03    | Professional transcripts |
| Azure OpenAI | Custom Whisper deployment | Varies   | Enterprise needs         |

---

## 🛠️ Troubleshooting

### **Common Issues**

- **CUDA Out of Memory**: Use smaller model (`--model base`)
- **File Not Found**: Check paths with `ls` before running
- **API Errors**: Verify your API keys are set correctly

### **Optimization Tips**

```bash
# Process large folders in batches (avoid OOM)
find ./audio -name "*.mp3" -exec python transcribe.py {} \;

# Compress audio for API limits (25MB)
ffmpeg -i input.wav -b:a 64k output.mp3
```

### **Azure-Specific Checks**

1. Verify your deployment name matches Azure portal
2. Check regional availability
3. Ensure proper role assignments

---

## 📜 License

MIT License - Free for personal/commercial use

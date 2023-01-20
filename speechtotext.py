
from speech_to_text import SpeechRecognitionModel

model = SpeechRecognitionModel("facebook/wav2vec2-large-960h-lv60-self")
audio_paths = ["out.wav"]
transcriptions = model.transcribe(audio_paths)
print(transcriptions)
    

from recognize_text_from_video import SpeechRecognitionModel
import pyperclip
import os

model = SpeechRecognitionModel("facebook/wav2vec2-base-100h")
audio_paths = ["out.wav"]
transcriptions = model.transcribe(audio_paths)
print(transcriptions)
transcriptstr = str(transcriptions)
pyperclip.copy(''.join(transcriptstr))
os.remove('out.wav')
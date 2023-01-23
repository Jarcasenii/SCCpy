from recognize_text_from_video import SpeechRecognitionModel
import pyperclip

model = SpeechRecognitionModel("facebook/wav2vec2-base-100h")
audio_paths = ["out.wav"]
transcriptions = model.transcribe(audio_paths)
print(transcriptions)
transcriptstr = str(transcriptions)
pyperclip.copy(''.join(transcriptstr))

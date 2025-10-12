import wave
from piper import PiperVoice, SynthesisConfig
import os
import sys


def generateTTS(path, tts):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    audioPath = path.replace(".txt", ".wav")
    tts.synthesize(text, audioPath)


class TTSProcessor:
    def __init__(self, voice_path=None):
        if voice_path is None:
            voice_path = os.path.join(
                os.path.dirname(__file__), "en_GB-alba-medium.onnx"
            )
        self.voice = PiperVoice.load(voice_path)

    def synthesize(self, text, output_path, speed=1):
        with wave.open(output_path, "wb") as wav_file:
            syn_config = SynthesisConfig(
                volume=1,
                length_scale=1 / speed,  # speed
                noise_scale=1.0,  # audio variation
                noise_w_scale=1.0,  # speaking variation
                normalize_audio=False,
            )
            self.voice.synthesize_wav(text, wav_file, syn_config=syn_config)


def main():
    if len(sys.argv) < 2:
        print("Usage: python piperTTS.py <input_text_file> [output_wav_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.wav"

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    tts = TTSProcessor()
    tts.synthesize(text, output_file)
    print(f"Audio saved to {output_file}")


if __name__ == "__main__":
    main()

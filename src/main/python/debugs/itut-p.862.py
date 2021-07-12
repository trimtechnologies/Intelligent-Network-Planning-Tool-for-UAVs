# import soundfile as sf
# from pypesq import pesq
#
#
# ref, sr = sf.read("./speech.wav")
# deg, sr = sf.read("./speech_bab_0dB.wav")
#
# score = pesq(ref, deg, sr)
# print(score)

# ------------------------------------------------

from scipy.io import wavfile
from pesq import pesq

rate, ref = wavfile.read("speech.wav")
rate, deg = wavfile.read("speech_bab_0dB.wav")

print(pesq(rate, ref, deg, 'wb'))
print(pesq(rate, ref, deg, 'nb'))

#----------------------------------------------------------------------------------------------------------------

import sounddevice as sd
from scipy.io import wavfile

def wav_play(filename):
    rate, data = wavfile.read(filename)
    sd.play(data, rate)
    sd.wait()  # Wait until the file is done playing
#----------------------------------------------------------------------------------------------------------------
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pyloudnorm as pyln

def wav_plot_3(file_path):
    # Load the audio file
    audio, sr = librosa.load(file_path, mono=True)

    # Compute LUFS
    meter = pyln.Meter(sr)  # create BS.1770 meter
    lufs = meter.integrated_loudness(audio)

    # Amplitude plot
    plt.figure(figsize=(15, 7))
    plt.subplot(3, 1, 1)
    librosa.display.waveshow(audio, sr=sr)
    plt.title(f'Amplitude - {file_path}')

    # LUFS plot
    plt.subplot(3, 1, 2)
    plt.bar(['LUFS'], [lufs])
    plt.title('Loudness (LUFS)')

    # Spectrogram
    plt.subplot(3, 1, 3)
    S = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)
    librosa.display.specshow(S, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Frequency Spectrogram')

    plt.tight_layout()
    plt.show()

#----------------------------------------------------------------------------------------------------------------

# function to write the audio 

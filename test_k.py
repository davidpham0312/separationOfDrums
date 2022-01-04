import numpy as np
import librosa as lb
import matplotlib.pyplot as plt
from librosa.display import specshow
from Separator import separate
import sys
import soundfile as sf


def test_different_iterations(filename, k_num, k_max):
    audio_org, fs_org = lb.load(filename, sr=None)

    sum_s_t = np.sum(np.power(audio_org, 2))
    snrH_array = np.zeros(k_num)
    snrP_array = np.zeros(k_num)

    snr_idx = 0
    i = 1

    plt.figure(figsize=(14, 7))
    k_arr = np.linspace(0, k_max, k_num)
    for k in k_arr:

        separate(filename, k_max=k)
        audioH, srH = lb.load("audioOut/H.wav", sr=None)
        audioP, srP = lb.load("audioOut/P.wav", sr=None)

        DH = lb.amplitude_to_db(np.abs(lb.stft(audioH)), ref=np.max)
        DP = lb.amplitude_to_db(np.abs(lb.stft(audioP)), ref=np.max)

        plt.subplot(len(k_arr), 2, i)
        specshow(DH, y_axis="linear")
        plt.colorbar(format='%+2.0f dB')
        plt.title('Harmonic power spectrogram with ' + str(k) + ' iterations')

        plt.subplot(len(k_arr), 2, i+1)
        specshow(DP, y_axis="linear")
        plt.colorbar(format='%+2.0f dB')
        plt.title('Percussion power spectrogram with ' + str(k) + ' iterations')

        i += 2

        sum_e_t_H = np.sum(np.power((audio_org - audioH), 2))
        sum_e_t_P = np.sum(np.power((audio_org - audioP), 2))

        snrH_array[snr_idx] = 10 * np.log10(sum_s_t / sum_e_t_H)
        snrP_array[snr_idx] = 10 * np.log10(sum_s_t / sum_e_t_P)
        snr_idx += 1

    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(k_arr, snrH_array, 'r-', label='Harmonic')
    plt.plot(k_arr, snrP_array, 'b-', label='Percussive')
    plt.xlabel('No. iterations')
    plt.ylabel('SNR')
    plt.legend()
    plt.title('SNR of harmonic and percussive components from file '
              + filename + ' with different no.iterations')
    plt.show()


if len(sys.argv) == 1:
    print("Please enter the audio filepath after the .py file")
    exit(0)
else:
    filename = sys.argv[1]
    k_num = int(input("Enter number of different iterations: "))
    k_max = int(input("Enter maximum number of iterations: "))
    test_different_iterations(filename, k_num, k_max)
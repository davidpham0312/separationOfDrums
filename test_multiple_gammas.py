import numpy as np
import librosa as lb
import matplotlib.pyplot as plt
from librosa.display import specshow
from Separator import calculate_delta, separate
import sys
import soundfile as sf

def test_different_gamma(filename, num_of_gamma):
    i = 0
    gammas = np.linspace(0, 1, num_of_gamma)
    audioO, srO = lb.load(filename, sr=None)

    # SNR arrays
    snr_h = np.zeros(num_of_gamma)
    snr_p = np.zeros(num_of_gamma)

    plt.figure(figsize=(14, 7))

    for gamma in gammas:
        # Separate into harmonics & percussion
        separate(filename, gamma=gamma)
        audioH, srH = lb.load('H.wav', sr=None)
        audioP, srP = lb.load('P.wav', sr=None)

        # Get the separated (harmonics-only & percussions-only) power spectrograms
        DH = lb.amplitude_to_db(np.abs(lb.stft(audioH)), ref=np.max)
        DP = lb.amplitude_to_db(np.abs(lb.stft(audioP)), ref=np.max)

        # Calculate the SNR
        snr_h[i] = 10 * np.log10(
            np.sum(np.power(audioO, 2)) / np.sum(np.power(audioO - audioH, 2)))
        snr_p[i] = 10 * np.log10(
            np.sum(np.power(audioO, 2)) / np.sum(np.power(audioO - audioP, 2)))

        # Plot the 2 separated spectrograms
        plt.subplot(num_of_gamma, 2, 2 * i + 1)
        specshow(DH, y_axis='linear')
        plt.colorbar(format='%+2.0f dB')
        plt.title(f'Harmonics , γ = {gamma:.2f}')
        plt.subplot(num_of_gamma, 2, 2 * i + 2)
        specshow(DP, y_axis='linear')
        plt.colorbar(format='%+2.0f dB')
        plt.title(f'Percussions, γ = {gamma:.2f}')

        i += 1

    plt.tight_layout()
    plt.show()

    # Plot the SNR of different gammas
    plt.figure(figsize=(10, 6))
    plt.plot(gammas, snr_h, 'r-', label='Harmonic')
    plt.plot(gammas, snr_p, 'b-', label='Percussive')
    plt.xlabel('γ')
    plt.ylabel('SNR')
    plt.legend()
    plt.title('SNR of harmonic and percussive components from file '
              + filename + ' with different γ')
    plt.show()

if len(sys.argv) == 1:
    print("Please enter the audio filepath after the .py file")
    exit(0)
else:
    filename = sys.argv[1]
    num_of_gamma = int(input("Enter number of γ: "))
    test_different_gamma(filename, num_of_gamma)

import numpy as np
import librosa as lb
import matplotlib.pyplot as plt
from librosa.display import specshow
import sys
import soundfile as sf


def calculate_delta(alpha, H, P):

    h = np.shape(H)[0]
    i = np.shape(H)[1]

    H_backward = np.concatenate((np.zeros((h,1)), H[:,0:(i-1)]), axis=1)
    H_forward = np.concatenate((H[:,1:i], np.zeros((h,1))), axis=1)

    P_downward = np.concatenate((np.zeros((1,i)), P[0:(h-1),:]), axis=0)
    P_upward = np.concatenate((P[1:h,:], np.zeros((1,i))), axis=0)

    delta = alpha * (H_backward - 2*H + H_forward)/4 - (1-alpha) * (P_downward - 2*P + P_upward)/4
    return delta


def separate(filename, gamma=1, a_h=1, a_p=1, k_max=20):
    """
    Separate an audio file into 2 audio files for
    harmonic and percussive components
    @params: filename: string - input audio file
             y: range compression coefficient (0 < y <= 1), which will be
                tested with different values in testPerformance.py. Here, it
                is set to 1
             a_h and a_p: weights of the horizontal and vertical smoothness
             k_max: number of iterations

    @return: 2 audio files "H.wav" and "P.wav" are created,
             which contain harmonic and percussive components, respectively,
             and saved into the specified directory.
    """
    # load the signal
    audioIn, fs = lb.load(filename, sr=None)

    # perform short-time Fourier transform
    n_fft = 2048
    n_audio = len(audioIn)
    F = lb.stft(audioIn, n_fft=n_fft)

    # Calculate a range-compressed version of the power spectrogram
    W = np.power(np.abs(F), 2*gamma)

    # Set initial values for harmonic and percussive power spectrogram
    H = W / 2
    P = W / 2
    k = 0
    a = np.power(a_p, 2) / (np.power(a_h, 2) + np.power(a_p, 2))

    while k < k_max - 1:
        delta = calculate_delta(a, H, P)

        H = H + delta
        H[H < 0] = 0
        np.copyto(H, W, where=(H > W))

        P = W - H
        k += 1

    # binarize separation output
    H = np.multiply((H >= P).astype('int'), W)
    P = np.multiply((H < P).astype('int'), W)
    # convert separated power spectrums back to waveform signals
    # by inverse short time Fourier transform
    x_h = lb.istft(H ** (1/2 * gamma) * np.exp(1j * np.angle(F)),
                   length=n_audio)
    x_p = lb.istft(P ** (1 / 2 * gamma) * np.exp(1j * np.angle(F)),
                   length=n_audio)

    sf.write("H.wav", x_h, fs)
    sf.write("P.wav", x_p, fs)


if len(sys.argv) == 1:
    print("Please enter the audio filepath after the .py file")
    exit(0)
else:
    filename = sys.argv[1]

    # Plot power spectrogram
    audioOG, srOG = lb.load(filename, sr=None)
    D = lb.amplitude_to_db(np.abs(lb.stft(audioOG)), ref=np.max)
    plt.figure(figsize=(7,6))
    plt.subplot(3, 1, 1)
    specshow(D, y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Power spectrogram of ' + filename)


    # Separate into harmonics & percussion
    separate(filename)
    audioH, srH = lb.load('H.wav', sr=None)
    audioP, srP = lb.load('P.wav', sr=None)

    # Get the separated (harmonics-only & percussions-only) power spectrograms
    DH = lb.amplitude_to_db(np.abs(lb.stft(audioH)), ref=np.max)
    DP = lb.amplitude_to_db(np.abs(lb.stft(audioP)), ref=np.max)

    # Plot the 2 separated spectrograms
    plt.subplot(3, 1, 2)
    specshow(DH, y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Power spectrogram of harmonics from ' + filename)
    plt.subplot(3, 1, 3)
    specshow(DP, y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Power spectrogram of percussions from ' + filename)
    plt.tight_layout()
    plt.show()

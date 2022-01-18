# Separation of drums #
## Description ##
The implementation aims to separate harmonic and percussive components of a music signals.
The directory contains all the input and output audio files, Python implementation as well as spectrograms and SNR analysis.

## Compilation ##
- Install necessary packages using pip:
    ```
    pip install numpy
    pip install librosa
    pip install matplotlib
    pip install soundfile
    ```
- Compile the separation program using the provided input audio file:
   ```
   python3 separator.py audioin/police03short.wav
   ```
- Test the audio with different number of iterations:
  ```
  python3 test_k.py audioin/police03short.wav
  ```
- Test the audio with different number of gammas:
  ```
  python3 test_multiple_gammas.py audioin/police03short.wav
  ```

## File structure ##

**audioIn**
  
- police03short.wav:        original audio file, including normal music with clear bass and drums.    
- project_test1.wav:        original audio file, including music and voice of a singer.
      
      
      
**audioOut**
  
- H.wav:                    Harmonic component audio file, will be overwritten if the 3 code files are executed.
- P.wav:                    Percussive component audio file, will be overwritten if the 3 code files are executed.
  
  
  
**Separator.py**:                
  - Separate harmonic and percussive components, with a auxiliary function calculate_delta.                    
  - Running this file with terminal requires a second parameter - an input audio file.
  				
          
  								
**test_multiple_gammas**:         
  - Test different ranges of compression (γ) while performing separation, which must be in the limit 0 <= γ <= 1. 
  - This file asks for how many values of γ will be used (which will be distributed linearly within the allowed range).
  				
  								
                  
**test_k.py**:                    
  - Test different values of number of iterations while performing separation, which must be in the limit 0 <= γ <= 1
  - This file asks for maximum value of k and how many k(s) will be used.



**analysis**
  
- SNR_k.png:                Signal-to-noise comparison between 5 k values, linearly from 0 to 50.
- SNR_gamma.png:            Signal-to-noise comparison between 5 gammas, linearly from 0 to 1.      
- PowSpec_5_k.png: 	        Power spectrogram of 5 k values, linearly from 0 to 50.      
- PowSpec_5_gammas.png:     Power spectrogram of 5 gamma values, linearly from 0 to 1.     
- PowerSpec_org_H_P.png:    Output power spectrograms of the file Separator.py with input file police03short.wav   
- PowSpec_other.png:        Output power spectrograms of the file Separator.py with input file project_test1.wav
  
  
  
**Report.pdf**:                   Project report.
  
  
**LICENSE**
  
  
**readme.md**

import pyaudio
import scipy as sp
import numpy as np
from scipy import signal

FORMAT = pyaudio.paFloat32
CHANNELS = 1 # Mono
FS = 44100 # or 48000, sampling rate
FRAME_SIZE = 2048 #512, 1024, 2048, 4096


# Autocorrelation Function
def ACF(sig, W, t, lag): #signal, window, timestep, # of sample shift
    ac = np.sum(
        sig[t : t + W] * sig[lag + t : lag + t + W]
    )
    return ac
    # Take the signal, window it and multiply it with a copy of itself... 
    # ...that's shifted by a # of samples
    # All bounds are shifted by the timestep value
    # Take the sum and return the value

# Difference Function
def DF(sig, W, t, lag):
    return ACF(sig, W, t, 0)\
    + ACF(sig, W, t + lag, 0)\
    - (2 * ACF(sig, W, t + lag, 0))

# Cumulative Mean Normalized Difference Function
def CMNDF(sig, W, t, lag): 
    if lag == 0:
        return 1

    return DF(sig, W, t, lag)\
        / np.sum([DF(sig, W, t, j + 1) for j in range(lag)] * lag)
        
def detect_pitch(sig, W, t, fs, bounds, threshold = 0.1): #bounds = limit the range of the search for detect_pitch
    # List of all lag values within the bounds
    CMNDF_values = [CMNDF(sig, W, t, i) for i in range(*bounds)] 
    print("reached this state")
    sample = None
    for i, val in enumerate(CMNDF_values):
        if val < threshold:
            sample = i + bounds[0]
            break
        if sample is None:
            sample = np.argmin(CMNDF_values) + bounds[0]

    #convert to frequency
    return fs / sample


def runloop(stream_in):
    window_size = 200
    bounds = [20, 2000]

    while True:
        stream_data = stream_in.read(FRAME_SIZE)
        samples = np.fromstring(stream_data, dtype = np.float32)

        if np.sum(samples) < 1e-10:
            continue

        pitches = []
        for i in range(samples.shape[0] // (window_size + 3)):
            pitches.append(
                detect_pitch(
                    samples,
                    window_size,
                    i * window_size,
                    FS,
                    bounds
                )
            )
        print([pitch for pitch in pitches])
        
def main():
    p = pyaudio.PyAudio()
    stream = p.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = FS,
        input = True,
        output = True,
        frames_per_buffer = FRAME_SIZE)

    try:
        runloop(stream)
    except KeyboardInterrupt:
        print('stopping stream')
        stream.stop_stream()
        stream.close()  

if __name__ == "__main__":
    main()
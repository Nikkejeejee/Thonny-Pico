from filefifo import Filefifo

data = Filefifo(10, name='capture_250Hz_01.txt')

first_sample = data.get()  # First value
prev_slope, peak_count, next_peak = 0, 0, 0

i = 0  # Number of samples processed
while data.has_data() and i < 250*10:  # Assuming 10s for 250Hz test sample and breaking loop
    nxt_sample = data.get()  # Get the next value
    cur_slope = nxt_sample - first_sample  #calculating slope
    
    if prev_slope > 0 and cur_slope <= 0: # Check if the slope changed from positive to negative
        peak_count += 1  # Stores the amount of peaks
        samples = i - next_peak
        seconds = samples / 250  # 250Hz sampling rate
        print(f"\nPeak {peak_count}: \n   {samples} samples,\n   {seconds:.3f} seconds")
        next_peak = i
    prev_slope = cur_slope  # Update previous slope and value
    first_sample = nxt_sample  # Updates the first sample to the current sample for the next iteration
    i += 1

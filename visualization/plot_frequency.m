#!/usr/bin/octave -qf
# This is for GNU octave, might also work with matlab

arg_list = argv();
[dir, name, ext, ver] = fileparts (arg_list{1});

# Load the data file
data = load(arg_list{1});

for ch = 1:60
   # Get one channel
   channel = data(:,ch);
   nSamples = length(channel);

   # Time signal, not used
   # t = (1/1000)*(1:nSamples);

   # Do the FFT
   y_fft = abs(fft(channel));

   # Chuck half of it (imaginary)
   y_fft = y_fft(1:nSamples/2);

   #Transpose so it matches the frequency range
   y_fft = y_fft';

   # Frequency range, 1000 is samples/second  
   f = 1000*(0:nSamples/2-1)/nSamples;

   #Draw some pretty pictures
   figure;
   plot(f, y_fft);
   set (gca, 'xtick', [0 60 100 200 300 400 500]);
   plotTitle = ["Channel " num2str(ch)];
   title(plotTitle);
   xlabel("Hz");
   ylabel("Amplitude");
   fname = ["./" name "_ch_" num2str(ch) "_fft.png"];
   print(1, fname);
   close(1);

endfor

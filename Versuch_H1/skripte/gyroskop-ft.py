import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks

# Read Gyroscope.csv file
df = pd.read_csv('data/Gyroscope.csv')

# Erstelle neue Zeitachse, die bei 0 beginnt
start_time = 20.3
df['Zeit_Angepasst'] = df['Time (s)'] - start_time

# Konvertiere die pandas Series zu NumPy-Arrays für die FFT
# Dies behebt den 'ALIGNED' KeyError
gyro_data = df['Gyroscope y (rad/s)'].to_numpy()

# Berechnung der Fourier-Transformation
N = len(gyro_data)
T = df['Zeit_Angepasst'].iloc[1] - df['Zeit_Angepasst'].iloc[0]  # Zeitintervall
yf = fft(gyro_data)  # Verwende NumPy-Array statt pandas Series
xf = fftfreq(N, T)[:N//2]

# Plot der Fourier-Transformation
fig, ax = plt.subplots(figsize=(10, 6))
amplitudes = 2.0/N * np.abs(yf[0:N//2])
ax.plot(xf, amplitudes, color='g')
ax.set_title('Fourier-Transformation von Gyroskop y')
ax.set_xlabel('Frequenz (Hz)')
ax.set_ylabel('Amplitude')
ax.set_xlim(0, 5)  # Frequenzen bis 5 Hz anzeigen
ax.set_ylim(0, 1.5)
ax.grid()

# Finden von Peaks in der Fourier-Transformation
peaks, _ = find_peaks(amplitudes, height=0.1)
ax.plot(xf[peaks], amplitudes[peaks], "x", color='r', markersize=10, label='Peaks')
ax.legend()
ax.set_ylim(0, 1)
#set x axis steps to 0.5
ax.xaxis.set_major_locator(plt.MultipleLocator(0.5))
ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))

# Annotieren der Peaks mit Frequenzen
for i, peak in enumerate(peaks):
    freq = xf[peak]
    amp = amplitudes[peak]
    # Vermeide Überlappungen bei der Textplatzierung
    y_offset = 0.3 + (i % 3) * 0.15  # Versetzte Positionen für bessere Lesbarkeit
    
    ax.annotate(f'Peak {i+1}: {freq:.3f} Hz', 
                xy=(freq, amp), 
                xytext=(freq, amp + y_offset),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1),
                fontsize=12, 
                color='r',
                ha='center')

plt.tight_layout()
plt.show()

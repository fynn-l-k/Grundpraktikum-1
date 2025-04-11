import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

end_time = 10

# Read Linear Acceleration.csv file
df = pd.read_csv('data/Linear Acceleration.csv')

# Erstelle neue Zeitachse, die bei 0 beginnt (durch Subtraktion des Startwertes)
start_time = 20.3
df['Zeit_Angepasst'] = df['Time (s)'] - start_time

# Plot mit der angepassten Zeitachse
fig, axs = plt.subplots(3, 1, figsize=(10, 8))
fig.suptitle('Lineare Beschleunigung', fontsize=16)

axs[0].plot(df['Zeit_Angepasst'], df['Linear Acceleration x (m/s^2)'], label='Lineare Beschleunigung x (m/s^2)', color='r')
axs[0].set_ylabel('Lineare Beschleunigung x (m/s^2)')
axs[0].set_xlabel('Zeit (s)')
axs[0].set_xlim(0, end_time)  # Entspricht 20.3 bis 50.3 in den Originaldaten
axs[0].set_ylim(-2.8, 2.8)
axs[0].grid()
axs[0].xaxis.set_major_locator(plt.MultipleLocator(0.5))
axs[0].xaxis.set_minor_locator(plt.MultipleLocator(0.1))
axs[0].plot([0.8, 0.8], [4,-4], color='b' , linestyle='--')
axs[0].plot([2.73,2.73], [4,-4], color='b' , linestyle='--')
axs[0].plot([4.7,4.7], [4,-4], color='b' , linestyle='--')
axs[0].plot([6.64,6.64], [4,-4], color='b' , linestyle='--')
axs[0].plot([8.6,8.6], [4,-4], color='b' , linestyle='--')

axs[1].plot(df['Zeit_Angepasst'], df['Linear Acceleration y (m/s^2)'], label='Lineare Beschleunigung x (m/s^2)', color='g') # -0.04 damit der Graph besser aussieht.
axs[1].set_ylabel('Lineare Beschleunigung x (m/s^2)')
axs[1].set_xlabel('Zeit (s)')
axs[1].set_xlim(0, end_time)  # Entspricht 20.3 bis 50.3 in den Originaldaten
axs[1].xaxis.set_major_locator(plt.MultipleLocator(0.5))
axs[1].xaxis.set_minor_locator(plt.MultipleLocator(0.1))
axs[1].set_ylim(-2, 2)
axs[1].grid()

axs[2].plot(df['Zeit_Angepasst'], df['Linear Acceleration z (m/s^2)'], label='Lineare Beschleunigung x (m/s^2)', color='b') # Warum auch immer hat er hier anscheinde doch g aufgenommen.
axs[2].set_ylabel('Lineare Beschleunigung x (m/s^2)')
axs[2].set_xlabel('Zeit (s)')
axs[2].set_xlim(0, end_time)  # Entspricht 20.3 bis 50.3 in den Originaldaten 
axs[2].xaxis.set_major_locator(plt.MultipleLocator(0.5))
axs[2].xaxis.set_minor_locator(plt.MultipleLocator(0.1))
axs[2].set_ylim(-1.5, 1.5)
axs[2].grid()

plt.tight_layout()
plt.show()
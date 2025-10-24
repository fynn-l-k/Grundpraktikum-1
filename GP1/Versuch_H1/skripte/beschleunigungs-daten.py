import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

end_time = 10


# Read Accelerometer.csv file
df = pd.read_csv('data/Accelerometer.csv')



# Erstelle neue Zeitachse, die bei 0 beginnt (durch Subtraktion des Startwertes)
start_time = 20.3
df['Zeit_Angepasst'] = df['Time (s)'] - start_time

# Plot mit der angepassten Zeitachse
fig, axs = plt.subplots(3, 1, figsize=(10, 8))
fig.suptitle('Beschleunigungsdaten', fontsize=16)

axs[0].plot(df['Zeit_Angepasst'], df['Acceleration x (m/s^2)'], label='Beschleunigung x (m/s^2)', color='r')
axs[0].set_ylabel('Beschleunigung x (m/s^2)')
axs[0].set_xlabel('Zeit (s)')
axs[0].set_xlim(0, end_time)  # Entspricht 20.3 bis 50.3 in den Originaldaten
axs[0].set_ylim(0, 2)
axs[0].grid()
axs[1].xaxis.set_major_locator(plt.MultipleLocator(0.5))
axs[1].xaxis.set_minor_locator(plt.MultipleLocator(0.1))

axs[1].plot(df['Zeit_Angepasst'], df['Acceleration y (m/s^2)'], label='Beschleunigung y (m/s^2)', color='g') # -0.04 damit der Graph besser aussieht.
axs[1].set_ylabel('Beschleunigung y (m/s^2)')
axs[1].set_xlabel('Zeit (s)')
axs[1].set_xlim(0, end_time)  # Entspricht 20.3 bis 50.3 in den Originaldaten
axs[1].set_ylim(-0.4, 0.4)
axs[1].grid()
axs[1].xaxis.set_major_locator(plt.MultipleLocator(0.5))
axs[1].xaxis.set_minor_locator(plt.MultipleLocator(0.1))
#axs[1].plot([1.9, 1.9], [1,-1], color='r' , linestyle='--')
#axs[1].plot([3.82,3.82], [1,-1], color='r' , linestyle='--')
#axs[1].plot([5.74,5.74], [1,-1], color='r' , linestyle='--')
#axs[1].plot([7.66,7.66], [1,-1], color='r' , linestyle='--')
#axs[1].plot([9.59,9.59], [1,-1], color='r' , linestyle='--')


axs[2].plot(df['Zeit_Angepasst'], df['Acceleration z (m/s^2)'], label='Beschleunigung z (m/s^2)', color='b')
axs[2].set_ylabel('Beschleunigung z (m/s^2)')
axs[2].set_xlabel('Zeit (s)')
axs[2].set_xlim(0, end_time)  # Entspricht 20.3 bis 50.3 in den Originaldaten 
axs[2].set_ylim(-1.5, 1.5)
axs[2].grid()
axs[1].xaxis.set_major_locator(plt.MultipleLocator(0.5))
axs[1].xaxis.set_minor_locator(plt.MultipleLocator(0.1))

plt.tight_layout()
plt.show()
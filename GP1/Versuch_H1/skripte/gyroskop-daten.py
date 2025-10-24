import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

end_time = 120

# Read Gyroscope.csv file
df = pd.read_csv('data/Gyroscope.csv')

# Erstelle neue Zeitachse, die bei 0 beginnt (durch Subtraktion des Startwertes)
start_time = 20.3
df['Zeit_Angepasst'] = df['Time (s)'] - start_time

# Plot mit der angepassten Zeitachse
fig, axs = plt.subplots(3, 1, figsize=(10, 8))
fig.suptitle('Gyroskopdaten', fontsize=16)

axs[0].plot(df['Zeit_Angepasst'], df['Gyroscope x (rad/s)'], label='Gyroskop x (rad/s)', color='r')
axs[0].set_ylabel('Gyroskop x (rad/s)')
axs[0].set_xlabel('Zeit (s)')
axs[0].set_xlim(0, end_time)  # Entspricht 20.3 bis 50.3 in den Originaldaten
axs[0].set_ylim(-0.25, 0.25)
axs[0].grid()

axs[1].plot(df['Zeit_Angepasst'], df['Gyroscope y (rad/s)'], label='Gyroskop y (rad/s)', color='g') # -0.04 damit der Graph besser aussieht.
axs[1].set_ylabel('Gyroskop y (rad/s)')
axs[1].set_xlabel('Zeit (s)')
axs[1].set_xlim(0, end_time)  # Entspricht 20.3 bis 50.3 in den Originaldaten
axs[1].set_ylim(-1.11, 1.11)
axs[1].grid()

axs[2].plot(df['Zeit_Angepasst'], df['Gyroscope z (rad/s)'], label='Gyroskop z (rad/s)', color='b') # Warum auch immer hat er hier anscheinde doch g aufgenommen.
axs[2].set_ylabel('Gyroskop z (rad/s)')
axs[2].set_xlabel('Zeit (s)')
axs[2].set_xlim(0, end_time)  # Entspricht 20.3 bis 50.3 in den Originaldaten 
axs[2].set_ylim(-1.5, 1.5)
axs[2].grid()


plt.tight_layout()
plt.show()
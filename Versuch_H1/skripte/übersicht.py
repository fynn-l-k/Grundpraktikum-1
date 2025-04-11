import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Gemeinsame Einstellungen
end_time = 120
start_time = 20.3

# 3x3 Subplot erstellen
fig, axs = plt.subplots(3, 3, figsize=(16, 12))
fig.suptitle('Sensordaten Vergleich', fontsize=18)

# Beschleunigungsdaten (Spalte 1)
df_acc = pd.read_csv('data/Accelerometer.csv')
df_acc['Zeit_Angepasst'] = df_acc['Time (s)'] - start_time

axs[0, 0].plot(df_acc['Zeit_Angepasst'], df_acc['Acceleration x (m/s^2)'], color='r')
axs[0, 0].set_title('Beschleunigung X')
axs[0, 0].set_ylabel('Beschleunigung (m/s²)')
axs[0, 0].set_xlim(0, end_time)
axs[0, 0].set_ylim(0, 2)
axs[0, 0].grid(True)

axs[1, 0].plot(df_acc['Zeit_Angepasst'], df_acc['Acceleration y (m/s^2)'] - 0.04, color='r')
axs[1, 0].set_title('Beschleunigung Y')
axs[1, 0].set_ylabel('Beschleunigung (m/s²)')
axs[1, 0].set_xlim(0, end_time)
axs[1, 0].set_ylim(-0.4, 0.4)
axs[1, 0].grid(True)

axs[2, 0].plot(df_acc['Zeit_Angepasst'], df_acc['Acceleration z (m/s^2)'] + 9.81, color='r')
axs[2, 0].set_title('Beschleunigung Z')
axs[2, 0].set_ylabel('Beschleunigung (m/s²)')
axs[2, 0].set_xlabel('Zeit (s)')
axs[2, 0].set_xlim(0, end_time)
axs[2, 0].set_ylim(-1.5, 1.5)
axs[2, 0].grid(True)

# Gyroskop-Daten (Spalte 2)
df_gyro = pd.read_csv('data/Gyroscope.csv')
df_gyro['Zeit_Angepasst'] = df_gyro['Time (s)'] - start_time

axs[0, 1].plot(df_gyro['Zeit_Angepasst'], df_gyro['Gyroscope x (rad/s)'], color='g')
axs[0, 1].set_title('Gyroskop X')
axs[0, 1].set_ylabel('Drehrate (rad/s)')
axs[0, 1].set_xlim(0, end_time)
axs[0, 1].set_ylim(-0.25, 0.25)
axs[0, 1].grid(True)

axs[1, 1].plot(df_gyro['Zeit_Angepasst'], df_gyro['Gyroscope y (rad/s)'], color='g')
axs[1, 1].set_title('Gyroskop Y')
axs[1, 1].set_ylabel('Drehrate (rad/s)')
axs[1, 1].set_xlim(0, end_time)
axs[1, 1].set_ylim(-1.11, 1.11)
axs[1, 1].grid(True)

axs[2, 1].plot(df_gyro['Zeit_Angepasst'], df_gyro['Gyroscope z (rad/s)'], color='g')
axs[2, 1].set_title('Gyroskop Z')
axs[2, 1].set_ylabel('Drehrate (rad/s)')
axs[2, 1].set_xlabel('Zeit (s)')
axs[2, 1].set_xlim(0, end_time)
axs[2, 1].set_ylim(-1.5, 1.5)
axs[2, 1].grid(True)

# Lineare Beschleunigungsdaten (Spalte 3)
df_lin = pd.read_csv('data/Linear Acceleration.csv')
df_lin['Zeit_Angepasst'] = df_lin['Time (s)'] - start_time

axs[0, 2].plot(df_lin['Zeit_Angepasst'], df_lin['Linear Acceleration x (m/s^2)'], color='b')
axs[0, 2].set_title('Lineare Beschleunigung X')
axs[0, 2].set_ylabel('Lin. Beschl. (m/s²)')
axs[0, 2].set_xlim(0, end_time)
axs[0, 2].set_ylim(-2.8, 2.8)
axs[0, 2].grid(True)

axs[1, 2].plot(df_lin['Zeit_Angepasst'], df_lin['Linear Acceleration y (m/s^2)'], color='b')
axs[1, 2].set_title('Lineare Beschleunigung Y')
axs[1, 2].set_ylabel('Lin. Beschl. (m/s²)')
axs[1, 2].set_xlim(0, end_time)
axs[1, 2].set_ylim(-2, 2)
axs[1, 2].grid(True)

axs[2, 2].plot(df_lin['Zeit_Angepasst'], df_lin['Linear Acceleration z (m/s^2)'], color='b')
axs[2, 2].set_title('Lineare Beschleunigung Z')
axs[2, 2].set_ylabel('Lin. Beschl. (m/s²)')
axs[2, 2].set_xlabel('Zeit (s)')
axs[2, 2].set_xlim(0, end_time)
axs[2, 2].set_ylim(-1.5, 1.5)
axs[2, 2].grid(True)

# Legende für die gesamten Spalten erstellen
handles = [
    plt.Line2D([0], [0], color='r', label='Rohbeschleunigung'),
    plt.Line2D([0], [0], color='g', label='Gyroskop'),
    plt.Line2D([0], [0], color='b', label='Lineare Beschleunigung')
]
fig.legend(handles=handles, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.01))

plt.tight_layout(rect=[0, 0.03, 1, 0.97])  # Anpassung für die Legende unten
plt.subplots_adjust(hspace=0.3, wspace=0.3)  # Abstand zwischen den Subplots erhöhen
plt.show()
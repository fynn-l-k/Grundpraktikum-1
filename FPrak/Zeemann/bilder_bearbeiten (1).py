from PIL import Image
import numpy as np

p = ["0_1", "0_2", "0_3", "0_4", "0_5", "0_6", "0_7", "0_8", "0_9", "1", "1_1", "1_2", "1_3", "1_4", "1_5", "1_6", "1_7", "1_8", "1_9", "2", "2_1", "2_2", "2_3", "2_4", "2_5", "2_6", "2_7", "2_8"]

for i in p:
    img = Image.open(f"./O43\Auflösevermögen\Zeemann_643_8nm_longitudinal/{i}A.tiff")
    arr = np.array(img).astype(float)

    # Graustufenbild (2D) oder RGB/RGBA (3D) abfangen
    gray = arr if arr.ndim == 2 else arr[:,:,0]

    # Gamma-Wert: höher = dunklerer Hintergrund
    GAMMA = 2.0

    norm = (gray - gray.min()) / (gray.max() - gray.min())
    norm_gamma = np.power(norm, GAMMA)
    green = (norm_gamma * 255).astype(np.uint8)

    rgb = np.zeros((green.shape[0], green.shape[1], 3), dtype=np.uint8)
    rgb[:,:,1] = green

    Image.fromarray(rgb).save(f"./O43\Auflösevermögen\Zeemann_643_8nm_longitudinal/{i}A_green.png")   
# C:\Users\vd01p\OneDrive\Desktop\Universität\Grundpraktikum-1\FPrak\Zeemann\O43\Auflösevermögen\Zeemann_643_8nm_longitudinal
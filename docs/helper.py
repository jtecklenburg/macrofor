def read_ppm_p6(filename):
    with open(filename, "rb") as f:
        # Header einlesen
        magic = f.readline().strip()
        if magic != b"P6":
            raise ValueError("Keine P6-Datei")

        # Kommentare überspringen
        def read_non_comment():
            line = f.readline()
            while line.startswith(b"#"):
                line = f.readline()
            return line

        # Breite, Höhe
        dims = read_non_comment().split()
        width, height = int(dims[0]), int(dims[1])

        # Maximalwert
        maxval = int(read_non_comment())
        if maxval > 255:
            raise ValueError("Nur 8-Bit unterstützt")

        # Pixeldaten einlesen
        data = f.read(width * height * 3)

    # In numpy-Array umwandeln
    import numpy as np
    img = np.frombuffer(data, dtype=np.uint8)
    img = img.reshape((height, width, 3))
    return img

# # Beispielaufruf
# image = read_ppm_p6("bild_p6.ppm")
# 
# # Mit matplotlib anzeigen
# import matplotlib.pyplot as plt
# plt.imshow(image)
# plt.show()

def _read_netpbm_header(f):
    """Read magic, width, height, maxval from an open binary PBM/PGM/PPM file."""
    def read_non_comment():
        line = f.readline()
        while line.startswith(b"#"):
            line = f.readline()
        return line

    magic = f.readline().strip()
    dims = read_non_comment().split()
    width, height = int(dims[0]), int(dims[1])
    maxval = int(read_non_comment())
    if maxval > 255:
        raise ValueError("Nur 8-Bit unterstützt")
    return magic, width, height


def read_pgm_p5(filename):
    """Read a binary PGM (P5) file and return a 2-D numpy uint8 array (height x width)."""
    import numpy as np
    with open(filename, "rb") as f:
        magic, width, height = _read_netpbm_header(f)
        if magic != b"P5":
            raise ValueError(f"Kein P5-Format, gefunden: {magic}")
        data = f.read(width * height)
    img = np.frombuffer(data, dtype=np.uint8).reshape((height, width))
    return img


def read_ppm_p6(filename):
    """Read a binary PPM (P6) file and return a 3-D numpy uint8 array (height x width x 3)."""
    import numpy as np
    with open(filename, "rb") as f:
        magic, width, height = _read_netpbm_header(f)
        if magic != b"P6":
            raise ValueError(f"Kein P6-Format, gefunden: {magic}")
        data = f.read(width * height * 3)
    img = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
    return img


def read_ppm_auto(filename):
    """Detect P5 or P6 automatically and return an appropriate numpy array."""
    import numpy as np
    with open(filename, "rb") as f:
        magic, width, height = _read_netpbm_header(f)
        if magic == b"P5":
            data = f.read(width * height)
            return np.frombuffer(data, dtype=np.uint8).reshape((height, width))
        elif magic == b"P6":
            data = f.read(width * height * 3)
            return np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
        else:
            raise ValueError(f"Unbekanntes Format: {magic}")

# # Beispielaufruf
# image = read_ppm_p6("bild_p6.ppm")
# 
# # Mit matplotlib anzeigen
# import matplotlib.pyplot as plt
# plt.imshow(image)
# plt.show()

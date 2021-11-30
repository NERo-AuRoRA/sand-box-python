import numpy as np
import cv2
from openni import openni2
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
openni2.initialize("./Redist")  # can also accept the path of the OpenNI redistribution

dev = openni2.Device.open_any()

depth_stream = dev.create_depth_stream()
depth_stream.start()
# Make data.
X = np.arange(0, 640, 1)
Y = np.arange(0, 480, 1)

X = X[80:]
Y = Y[10:480]

X, Y = np.meshgrid(X, Y)
frame = depth_stream.read_frame()
frame_data = frame.get_buffer_as_uint16()

img = np.frombuffer(frame_data, dtype=np.uint16)
Z = np.reshape(img, (480, 640))
Z = Z[10:480, 80:]

img.shape = (1, 480, 640)
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=True)
ax.zaxis.set_major_formatter('{x:.02f}')
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

while True:
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()

    img = np.frombuffer(frame_data, dtype=np.uint16)
    img.shape = (1, 480, 640)

    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 0, 1)

    # ==========================================================================================
    # OPÇÔES PARA CONVERSÂO DE IMAGENS PARA APLICAR COLORMAP
    # img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # img = (img/256).astype(np.uint8)
    # ==========================================================================================
    img = cv2.convertScaleAbs(img, alpha=0.1)  # alterando valor de alpha, altera-se o gradiente

    im_color = cv2.applyColorMap(img, cv2.COLORMAP_JET)  # APLIC-SE GRADIENTE

    cv2.imshow("image", im_color)
    cv2.waitKey(34)
depth_stream.stop()
openni2.unload()
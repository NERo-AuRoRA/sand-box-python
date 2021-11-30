import numpy as np
import cv2
from openni import openni2

openni2.initialize("./Redist")

dev = openni2.Device.open_any()

depth_stream = dev.create_depth_stream()
depth_stream.start()

while True:
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()

    img = np.frombuffer(frame_data, dtype=np.uint16)
    img.shape = (1, 480, 640)

    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 0, 1)
    print(img)
    # ==========================================================================================
    # OPÇÔES PARA CONVERSÂO DE IMAGENS PARA APLICAR COLORMAP
    # img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # img = (img/256).astype(np.uint8)
    # ==========================================================================================
    img = cv2.convertScaleAbs(img, alpha=0.1)  # alterando valor de alpha, altera-se o gradiente

    im_color = cv2.applyColorMap(img, cv2.COLORMAP_HOT)  # APLIC-SE GRADIENTE

    cv2.imshow("image", im_color)
    cv2.waitKey(34)

depth_stream.stop()
openni2.unload()

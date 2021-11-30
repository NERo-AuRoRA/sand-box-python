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
    img = np.concatenate(((img * 50), (img * 50), (img * 50)), axis=0)
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 0, 1)
    print(img)

    cv2.imshow("image", img)
    cv2.waitKey(34)

depth_stream.stop()
openni2.unload()

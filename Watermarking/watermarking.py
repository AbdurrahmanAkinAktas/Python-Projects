import cv2
import os
import numpy as np


original = cv2.imread('original_image.png')
watermark = cv2.imread('watermark.png', 0)

watermark = cv2.resize(watermark, (original.shape[1], original.shape[0]))

cv2.imwrite('resized_watermark.png', watermark)

# set 3 LSBs of RGB channels to 0
to_zero = 0b11111000

output = np.bitwise_and(original, to_zero)

output = np.moveaxis(output, -1 ,0)

output[0] = np.bitwise_or(output[0], np.right_shift(np.bitwise_and(watermark, 0b11100000), 5))
output[1] = np.bitwise_or(output[1], np.right_shift(np.bitwise_and(watermark, 0b00011100), 2))
output[2] = np.bitwise_or(output[2], np.bitwise_and(watermark, 0b00000011))

output = np.moveaxis(output, 0,-1)

cv2.imwrite('output.png', output)

# extract the watermark back out to confirm it worked

output = np.moveaxis(output, -1 ,0)

extracted = np.zeros((original.shape[0], original.shape[1]), dtype=np.uint8)


# shifted = np.left_shift(output[0], 5)
# anded = np.bitwise_and(shifted, 0b11100000)
# print(anded.shape)
# extracted = np.bitwise_or(extracted, anded)

extracted = np.bitwise_or( extracted, (np.bitwise_and(np.left_shift(output[0], 5), 0b11100000)))
extracted = np.bitwise_or( extracted, np.bitwise_and(np.left_shift(output[1], 2), 0b00011100))
extracted = np.bitwise_or( extracted, np.bitwise_and(output, 0b00000011))

extracted = np.moveaxis(extracted, 0,-1)

print(extracted.shape)

cv2.imwrite('extracted.png', extracted)
cv2.imshow('test', extracted)

k = cv2.waitKey(0)
cv2.destroyAllWindows()
import numpy as np
import cv2

def apply_cool_tone(image: np.ndarray) -> np.ndarray:
    """
    Apply a cool tone filter to the image by manually adjusting the weights of RGB channels.
        
    :param image: Input image in BGR format (height, width, 3).
    :return: Image with cool tone filter applied.
    """
    if len(image.shape) == 2:
    # แปลงจาก grayscale เป็น RGB
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)


    R = image[:, :, 2]  # Red channel
    G = image[:, :, 1]  # Green channel
    B = image[:, :, 0]  # Blue channel

    #การทำให้ภาพเป็นโทนเย็นนั้น จะต้องเน้นเฉดสีฟ้า (Blue) และสีเขียว (Green) โดยลดโทนสีแดง (Red) ซึ่งเป็นโทนสีร้อนที่ทำให้ภาพดูอบอุ่นหรือสว่าง

        #np.clip เป็นการ limit values ให้อยู๋ในrangeที่ต้องการ {syntax : np.clip(arr, min_value, max_value)}
    R = np.clip(R * 0.8, 0, 255)   #decrease red 10%
    G = np.clip(G * 1.05, 0, 255)   #increase green 10%
    B = np.clip(B * 1.25, 0, 255)   #increase blue 20%
                            #np.dstack เป็นการนำ array มาmergeกัน {syntax : np.dstack((arr1, arr2, ...))}
    cool_tone_image = np.dstack((B, G, R)).astype(np.uint8)   #ลำดับใน dstack(B, G, R) เสมอ

    return cool_tone_image
    
def apply_warm_tone(image: np.ndarray) -> np.ndarray:
    """
    Apply a warm tone filter to the image by adjusting the weights of RGB channels.
    
    :param image: Input image in BGR format (height, width, 3).
    :return: Image with warm tone filter applied.
    """
    if len(image.shape) == 2:
    # แปลงจาก grayscale เป็น RGB
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    R = image[:, :, 2]  # Red channel
    G = image[:, :, 1]  # Green channel
    B = image[:, :, 0]  # Blue channel

    R = np.clip(R * 1.3, 0, 255)   #increase red 20%
    G = np.clip(G * 1.05, 0, 255)   #increase green 10%
    B = np.clip(B * 0.85, 0, 255)   #decrease blue 10%

    warm_tone_image = np.dstack((B, G, R)).astype(np.uint8)

    return warm_tone_image
    
def apply_vintage_tone(image: np.ndarray) -> np.ndarray:
    """
    Apply a vintage tone filter to the image to give it a brown, aged look.
    """
    if len(image.shape) == 2:
    # แปลงจาก grayscale เป็น RGB
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)


    B = image[:, :, 0] * 0.5  # ลดความเข้มของสีฟ้าอย่างมาก
    G = image[:, :, 1] * 0.7  # ลดความเข้มของสีเขียว
    R = image[:, :, 2] * 1.2  # เพิ่มความเข้มของสีแดง

    # เพิ่มความเป็นสีเหลืองโดยเพิ่มค่าสีแดงและสีเขียวเล็กน้อย
    B = np.clip(B, 0, 255)
    G = np.clip(G + 30, 0, 255)  # เพิ่มสีเขียวเพื่อให้เกิดสีน้ำตาล
    R = np.clip(R + 15, 0, 255)  # เพิ่มสีแดงเล็กน้อยเพื่อเสริมเอฟเฟกต์เก่า

    vintage_tone_image = np.dstack((B, G, R)).astype(np.uint8)

    return vintage_tone_image
    
def apply_high_contrast(image: np.ndarray) -> np.ndarray:
    contrast_image = np.clip(image * 1.5 - 50, 0, 255)
    return contrast_image.astype(np.uint8)



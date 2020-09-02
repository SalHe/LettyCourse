import cv2
import easyocr

en_reader: easyocr.Reader
ch_reader: easyocr.Reader


def init():
    # Init ocr
    global ch_reader
    global en_reader
    ch_reader = easyocr.Reader(['ch_sim', 'en'])
    en_reader = easyocr.Reader(['en'])


def handle_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.adaptiveThreshold(~img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

    h_img = img.copy()
    v_img = img.copy()
    scale = 15
    h_size = int(h_img.shape[1] / scale)

    h_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (h_size, 1))  # 形态学因子
    h_erode_img = cv2.erode(h_img, h_structure, 1)

    h_dilate_img = cv2.dilate(h_erode_img, h_structure, 1)
    v_size = int(v_img.shape[0] / scale)

    v_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, v_size))  # 形态学因子
    v_erode_img = cv2.erode(v_img, v_structure, 1)
    v_dilate_img = cv2.dilate(v_erode_img, v_structure, 1)

    mask_img = h_dilate_img + v_dilate_img
    return mask_img

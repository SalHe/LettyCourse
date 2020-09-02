import cv2
import easyocr
import numpy as np
import re
from aip import AipOcr
from LettySchool.CourseApi import CourseInfo
from LettySchool.CourseApi import CourseTime

en_reader: easyocr.Reader
ch_reader: easyocr.Reader


def init():
    # Init ocr
    global ch_reader
    global en_reader
    ch_reader = easyocr.Reader(['ch_sim', 'en'])
    en_reader = easyocr.Reader(['en'])


def get_image_mask(img):
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


class DetectTable(object):
    def __init__(self, src_img):
        self.src_img = src_img

    def run(self) -> (np.ndarray, np.ndarray):
        if len(self.src_img.shape) == 2:  # 灰度图
            gray_img = self.src_img
        elif len(self.src_img.shape) == 3:
            gray_img = cv2.cvtColor(self.src_img, cv2.COLOR_BGR2GRAY)

        thresh_img = cv2.adaptiveThreshold(~gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
        h_img = thresh_img.copy()
        v_img = thresh_img.copy()
        scale = 15
        h_size = int(h_img.shape[1] / scale)

        h_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (h_size, 1))  # 形态学因子
        h_erode_img = cv2.erode(h_img, h_structure, 1)

        h_dilate_img = cv2.dilate(h_erode_img, h_structure, 1)
        # cv2.imshow("h_erode",h_dilate_img)
        v_size = int(v_img.shape[0] / scale)

        v_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, v_size))  # 形态学因子
        v_erode_img = cv2.erode(v_img, v_structure, 1)
        v_dilate_img = cv2.dilate(v_erode_img, v_structure, 1)

        mask_img = h_dilate_img + v_dilate_img
        joints_img = cv2.bitwise_and(h_dilate_img, v_dilate_img)
        # cv2.imshow("joints", joints_img)
        # cv2.imshow("mask", mask_img)

        return mask_img, joints_img


def analyse_schedule(img):
    aip_client = AipOcr('22509825', 'asIuPLqcoAl6gryqAWicZcUI', 'f3a9dooKh3fzb1gVS7pj0j42alXNVhRn')

    hh = 0
    bh = 0
    left = [0]
    mask, joints = DetectTable(img).run()

    # Determine the height of header and one row
    for y in range(1, joints.shape[0]):
        if joints[y, 0] == 255:
            if hh == 0:
                hh = y
            else:
                bh = y - hh
                break

    # Determine the width of each column
    for x in range(1, joints.shape[1]):
        if joints[0, x] == 255:
            left.append(x)

    def clip(raw, col):
        s, i = cv2.imencode('.jpg',
                            img[hh + raw * bh + 1:hh + (raw + 1) * bh, left[col] + 1: left[col + 1]])
        return s, i

    def ocr(clip_result, filter_char=True):
        if clip_result[0]:
            res = aip_client.basicAccurate(clip_result[1])
            s = res['words_result'][0]['words']
            if filter_char:
                s = filter_useless_char(s)
            return s
        return ''

    def delay():
        import time
        time.sleep(0.5)

    for y in range(0, (joints.shape[0] - hh) // bh):
        new_course = CourseInfo()

        # code, name
        reg_result = re.search(r'^(\d+)(.+)', ocr(clip(y, 0)))
        new_course.code = reg_result.group(1)
        new_course.name = reg_result.group(2)
        delay()

        # points
        new_course.points = float(ocr(clip(y, 1), filter_char=False))
        delay()

        # periods
        new_course.periods = float(ocr(clip(y, 2), filter_char=False))
        delay()

        # check_method
        new_course.check_method = ocr(clip(y, 3))
        delay()

        # teacher
        new_course.teacher = ocr(clip(y, 4))
        delay()

        # number
        new_course.number = ocr(clip(y, 5))
        delay()

        # population
        new_course.population = int(ocr(clip(y, 6), filter_char=False))
        delay()

        # weeks
        s = ocr(clip(y, 7), filter_char=False)
        s = s.replace('.', '')
        s = s.split('-')
        new_course.weeks = range(int(s[0]), int(s[1]) + 1)
        delay()

        # time
        s = ocr(clip(y, 8), filter_char=False)
        s = re.search(r'(.+)[(\d+)\-(\d+)节]', s)
        time = CourseTime(
            day=s.group(1),
            range=range(int(s.group(2)), s.group(3)))
        new_course.time.append(time)

        # location
        new_course.location = ocr(clip(y, 9))
        delay()

        print(new_course)


def filter_useless_char(s):
    for char in '[]:!@#$%^&*()_+~<>?:"|\\\';/.,':
        s = s.replace(char, '')
    return s

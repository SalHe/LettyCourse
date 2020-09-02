import LettySchool
from LettySchool.CourseApi import *
from LettySchool import Ocr
from retrying import retry

import os
import cv2

img_dir = os.path.join(os.curdir, 'img')
captcha_dir = os.path.join(img_dir, 'captcha')
for dir_ in (img_dir, captcha_dir):
    if not os.path.isdir(dir_):
        os.mkdir(dir_)

c = CourseApi(LettySchool.TYPE_LIST)


def save_image(img, path, open_img=False):
    cv2.imwrite(path, img)
    if open_img:
        cv2.imshow(path, img)
        cv2.waitKey()


@retry(stop_max_attempt_number=10)
def verify_captcha():
    print('正在获取验证码...')
    c.get_captcha()

    # OCR
    print('正在处理验证码...')
    captcha_img = Ocr.handle_image(c.captcha_image)
    print('正在尝试识别验证码...')
    for reader in (Ocr.en_reader, Ocr.ch_reader):
        code = reader.readtext(captcha_img, detail=0)

        codes = [''.join(code)]

        code.reverse()
        codes.append(''.join(code))

        for code in codes:
            ok, w, h = c.verify_captcha(code)
            if ok:
                # cv2.imshow(code, captcha_img)
                # cv2.waitKey()
                print('✔验证码正确')
                return
            else:
                print('✖验证码识别错误')
                save_image(captcha_img, os.path.join(captcha_dir, code + '.jpg'))

    raise Exception('✖验证码错误')


@retry(stop_max_attempt_number=10)
def fetch_schedule():
    verify_captcha()
    schedule_img = c.get_schedule()
    save_image(schedule_img, './table.jpg', open_img=True)


if __name__ == '__main__':
    Ocr.init()
    fetch_schedule()

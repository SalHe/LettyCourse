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
    error_codes = []
    for reader in (Ocr.en_reader, Ocr.ch_reader):
        code = reader.readtext(captcha_img, detail=0)

        codes = [''.join(code)]

        code.reverse()
        codes.append(''.join(code))

        for code in codes:
            if code in error_codes:
                continue
            ok, w, h = c.verify_captcha(code)
            if ok:
                # cv2.imshow(code, captcha_img)
                # cv2.waitKey()
                print('✔验证码正确')
                return
            else:
                error_codes.append(code)
                path = os.path.join(captcha_dir, code + '.jpg')
                print(f'✖验证码识别错误, 已保存到{path}')
                save_image(captcha_img, path)

    raise Exception('✖验证码错误')


@retry(stop_max_attempt_number=10)
def fetch_schedule():
    print('正在尝试通过验证码...')
    verify_captcha()
    print('正在下载课表...')
    schedule_img = c.get_schedule()
    save_image(schedule_img, './table.jpg', open_img=True)


if __name__ == '__main__':
    print('正在初始化OCR')
    Ocr.init()
    print('开始获取课表')
    fetch_schedule()

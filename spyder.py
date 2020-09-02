# -*-coding:utf-8-*-

import LettySchool
from LettySchool.CourseApi import *
from LettySchool import Ocr
from retrying import retry

import os
import cv2


def save_image(img, path, open_img=False):
    cv2.imencode('.jpg',img)[1].tofile(path)
    if open_img:
        cv2.imshow(path.encode('gbk').decode(errors='ignore'), img)
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
    class_name = ''
    for class_info in class_list:
        if class_info.code == c.class_code:
            class_name = class_info.tip
            break
    path = os.path.join(schedule_dir, class_name + '.jpg')
    path = os.path.abspath(path)
    save_image(schedule_img, path, open_img=True)
    print(f'课表下载成功，保存到{path}')


if __name__ == '__main__':
    # Init dirs
    img_dir = os.path.join(os.curdir, 'img')
    captcha_dir = os.path.join(img_dir, 'captcha')
    schedule_dir = os.path.join(img_dir, 'schedule')
    for dir_ in (img_dir, captcha_dir, schedule_dir):
        if not os.path.isdir(dir_):
            os.mkdir(dir_)

    # Init api
    c = CourseApi(LettySchool.TYPE_LIST)
    year_term_list, class_list = CourseApi.load_selections()

    print('正在初始化OCR')
    Ocr.init()
    print('开始获取课表')
    fetch_schedule()

    mask = Ocr.handle_image(c.schedule_image)

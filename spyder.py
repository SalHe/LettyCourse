from LettySchool.CourseApi import *
from LettySchool import Ocr

import cv2


def save_image(img, path, open_img=False):
    cv2.imwrite(path, img)
    if open_img:
        cv2.imshow(path, img)
        cv2.waitKey()


if __name__ == '__main__':
    Ocr.init()

    # Fetch captcha
    c = CourseApi(TYPE_TABLE)
    c.get_captcha()

    # Input code
    # print("请输入验证码：")
    # code = input()
    captcha_img = Ocr.handle_image(c.captcha_image)
    code = Ocr.en_reader.readtext(captcha_img, detail=0)
    code.reverse()
    code = ''.join(code)
    ok, w, h = c.verify_captcha(code)
    if not ok:
        cv2.imshow(code, captcha_img)
        cv2.waitKey()
        print('✖验证码错误')
        exit(1)

    print('✔验证码正确')
    # Fetch table
    schedule_img = c.get_schedule()
    save_image(schedule_img, './table.jpg', open_img=True)

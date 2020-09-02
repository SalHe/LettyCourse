from LettySchool import course
import cv2


def save_and_open_image(img, path):
    with open(path, "wb") as f:
        f.write(img)
        f.close()
    img = cv2.imread(path)
    cv2.imshow(path, img)
    cv2.waitKey()


if __name__ == '__main__':
    # Fetch captcha
    c = course.Course(course.TYPE_TABLE)
    captcha_img = c.get_captcha()
    save_and_open_image(captcha_img, "./captcha.jpg")

    # Input code
    print("请输入验证码：")
    code = input()
    c.verify_captcha(code)

    # Fetch table
    schedule_img = c.get_schedule()
    save_and_open_image(schedule_img, "./table.jpg")

from LettySchool import course
from PIL import Image


def save_and_open_image(img, path):
    with open(path, "wb") as f:
        f.write(img)
        f.close()
    Image.open(path).show()


def main():
    # Fetch captcha
    c = course.Course()
    captcha_img = c.get_captcha()
    save_and_open_image(captcha_img, "./captcha.jpg")

    # Input code
    print("请输入验证码：")
    code = input()
    c.verify_captcha(code)

    # Fetch table
    schedule_img = c.get_schedule()
    save_and_open_image(schedule_img, "./table.jpg")


if __name__ == '__main__':
    main()

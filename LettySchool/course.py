import requests
import utils


class Course:
    def __init__(self):
        self.cookies = {}

    def get_captcha(self) -> bytes:
        headers = {
            "Cache-Control": "max-age:0",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "http://222.87.37.94",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q:0.9,image/webp,image/apng,*/*;q:0.8,application/signed-exchange;v:b3;q:0.9",
            "Referer": "http://222.87.37.94/jwweb/ZNPK/KBFB_ClassSel.aspx",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en,zh-CN;q:0.9,zh;q:0.8,ja-CN;q:0.7,ja;q:0.6,en-CN;q:0.5"
        }
        respone = requests.get("http://222.87.37.94/jwweb/sys/ValidateCode.aspx",
                               params={
                                   "t": utils.getCurTimestamp(True)
                               },
                               headers=headers,
                               cookies=self.cookies)
        self.cookies.update(respone.cookies)
        return respone.content

    def verify_captcha(self, captcha_code):
        headers = {
            "Cache-Control": "max-age:0",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "http://222.87.37.94",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q:0.9,image/webp,image/apng,*/*;q:0.8,application/signed-exchange;v:b3;q:0.9",
            "Referer": "http://222.87.37.94/jwweb/ZNPK/KBFB_ClassSel.aspx",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en,zh-CN;q:0.9,zh;q:0.8,ja-CN;q:0.7,ja;q:0.6,en-CN;q:0.5",
        }
        respone = requests.post("http://222.87.37.94/jwweb/ZNPK/KBFB_ClassSel_rpt.aspx",
                                data={
                                    "Sel_XNXQ": "20200",
                                    "txtxzbj": "",
                                    "Sel_XZBJ": "2019060503",
                                    "type": "1",
                                    "txt_yzm": captcha_code
                                },
                                cookies=self.cookies,
                                headers=headers)
        self.cookies.update(respone.cookies)

    def get_schedule(self) -> bytes:
        respone = requests.get(
            'http://222.87.37.94/jwweb/ZNPK/drawkbimg.aspx?type=1&w=1110&h=400&xn=2020&xq=0&bjdm=2019060503',
            cookies=self.cookies,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
                "Accept": "image/webp,image/apng,image/*,*/*;q:0.8",
                "Referer": "http://222.87.37.94/jwweb/ZNPK/KBFB_ClassSel_rpt.aspx",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en,zh-CN;q:0.9,zh;q:0.8,ja-CN;q:0.7,ja;q:0.6,en-CN;q:0.5"
            })
        self.cookies.update(respone.cookies)
        return respone.content

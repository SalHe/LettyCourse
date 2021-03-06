from typing import List

import LettySchool
import requests
import utils
import cv2
import numpy as np
from lxml import etree
from dataclasses import dataclass


@dataclass
class YearTerm:
    year: str
    term: str
    tip: str


@dataclass
class ClassInfo:
    code: str
    tip: str


@dataclass
class CourseTime:
    day: str
    range: range


@dataclass
class CourseInfo:
    code: str
    name: str
    points: float
    periods: float
    check_method: str
    teacher: str
    number: str
    population: int
    weeks: str
    time: List[CourseTime]
    location: str

    def __init__(self):
        pass


class CourseApi:
    def __init__(self, img_type=LettySchool.TYPE_TABLE, exclude_public=False, year=2020, term=0,
                 class_code='2019060503'):
        self.cookies = {}

        self.type = img_type
        self.exclude_public = exclude_public

        self.year = year
        self.term = term
        self.class_code = class_code

        self.img_width = 0
        self.img_height = 0

        self.captcha_image = None
        self.schedule_image = None

    @staticmethod
    def load_selections() -> (List[YearTerm], List[ClassInfo]):
        response = requests.get('http://222.87.37.94/jwweb/ZNPK/KBFB_ClassSel.aspx')
        html: etree._Element = etree.HTML(response.content)

        # Year term
        year_term_list = []
        options = html.xpath("//select[@name='Sel_XNXQ']/option")
        for op in options:
            year = op.attrib['value'][0:4]
            term = op.attrib['value'][-1:]
            tip = op.text
            year_term_list.append(YearTerm(year, term, tip))

        # Class
        class_list = []
        options = html.xpath("//select[@name='Sel_XZBJ']/option")
        for op in options:
            class_list.append(ClassInfo(op.attrib['value'], op.text))

        return year_term_list, class_list

    def get_captcha(self):
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
        response = requests.get("http://222.87.37.94/jwweb/sys/ValidateCode.aspx",
                                params={
                                    "t": utils.getCurTimestamp(True)
                                },
                                headers=headers,
                                cookies=self.cookies)
        self.cookies.update(response.cookies)
        self.captcha_image = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
        return self.captcha_image

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
        response = requests.post("http://222.87.37.94/jwweb/ZNPK/KBFB_ClassSel_rpt.aspx",
                                 data={
                                     "Sel_XNXQ": f'{self.year}{self.term}',
                                     "txtxzbj": "",
                                     "Sel_XZBJ": self.class_code,
                                     "type": self.type,
                                     "txt_yzm": captcha_code
                                 },
                                 cookies=self.cookies,
                                 headers=headers)
        self.cookies.update(response.cookies)
        doc = etree.HTML(response.content)
        img = doc.xpath('//img')
        if len(img) > 0:
            img = img[0]
            self.img_width = img.attrib['width']
            self.img_height = img.attrib['height']
        else:
            self.img_width = self.img_height = 0
        return self.img_width != 0, self.img_width, self.img_height

    def get_schedule(self):
        response = requests.get(
            'http://222.87.37.94/jwweb/ZNPK/drawkbimg.aspx',
            params={
                'type': self.type,
                'w': self.img_width,
                'h': self.img_height,
                'xn': self.year,
                'xq': self.term,
                'bjdm': self.class_code,
                'rxflag': '1' if self.exclude_public else '0'
            },
            cookies=self.cookies,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
                "Accept": "image/webp,image/apng,image/*,*/*;q:0.8",
                "Referer": "http://222.87.37.94/jwweb/ZNPK/KBFB_ClassSel_rpt.aspx",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en,zh-CN;q:0.9,zh;q:0.8,ja-CN;q:0.7,ja;q:0.6,en-CN;q:0.5"
            })
        self.cookies.update(response.cookies)
        self.schedule_image = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
        return self.schedule_image

from selenium import webdriver
import os
import sys
from time import sleep
import logging
import logging.handlers

LOG_FILENAME = 'maotai.log'

logger = logging.getLogger(__name__)

def set_logger():
    # logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
    logging_format += "%(module)s::%(funcName)s():1%(lineno)d: %(message)s"
    logging_formater = logging.Formatter(logging_format)
    console_handler = logging.StreamHandler()
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
    console_handler.setFormatter(logging_formater)
    file_handler.setFormatter(logging_formater)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def set_basic_firefox_option():
    options = webdriver.firefox.options.Options()
    # incase need browser lunch, mark following line
    options.headless = True
    return options

set_logger()

def open_image(image_file):
    if os.name == "nt":
        os.system('start ' + image_file)
    else:
        if os.uname()[0] == "Linux":
            if "deepin" in os.uname()[2]:
                os.system("deepin-image-viewer " + image_file)
            else:
                os.system("eog " + image_file)
        else:
            os.system("open " + image_file)


def save_image(img, image_file):
    with open(image_file, 'wb') as pic:
        pic.write(img)


class JDMaotai():
    MAX_LOGIN_WAIT = 300
    def __init__(self):
        options = set_basic_firefox_option()
        self.driver = webdriver.Firefox(options=options)
        self.login = False

    
    def jd_login(self):
        logger.info("登陆京东")
        self.driver.get(r"https://passport.jd.com/new/login.aspx")

        qcr_login = self.driver.find_element_by_class_name("qrcode-login")
        img = qcr_login.find_element_by_tag_name("img")
        save_image(img.screenshot_as_png, "jd.png")
        open_image("jd.png")
        logger.info("请用京东手机APP扫一扫二维码")
        login_pause = self.MAX_LOGIN_WAIT

        while self.driver.current_url != 'https://www.jd.com/' and login_pause > 0:
            sleep(1)
            login_pause -= 1
        logger.info("登陆成功")

    def reserve(self):
        if not self.login:
            self.jd_login()
        logger.info("预约茅台")
        self.driver.get(r"https://item.jd.com/100012043978.html")
        btn_resrv = self.driver.find_element_by_id("btn-reservation")
        btn_resrv.click()
        logger.info("预约成功")

    def buy(self):
        if not self.login:
            self.jd_login()
        logger.info("购买茅台")
        # TODO
        # 找到京东茅台购买页面完善购买流程
        logger.info("购买成功")



if __name__ == "__main__":
    prompt = """                                                                             
    1.预约茅台
    2.抢购茅台
    """
    print(prompt)
    maotai = JDMaotai()
    choice_function = input('请选择:')
    if choice_function == '1':
        maotai.reserve()
    elif choice_function == '2':
        maotai.buy()
    else:
        print('没有此功能')
        sys.exit(1)

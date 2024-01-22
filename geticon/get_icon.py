import base64
import os
from typing import List
from urllib.parse import urljoin
from urllib.parse import urlparse

import magic
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

ua = UserAgent()


def is_data_url(url):
    return url.startswith('data:')


def is_relative_url(url):
    if url.startswith('http://') or url.startswith('https://') or url.startswith('//'):
        return False
    if url.startswith('data:'):
        return False


def is_absolute(url):
    """ Determine whether URL is absolute or relative """
    return bool(urlparse(url).netloc)


def get_base_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def get_hostname(url):
    parsed = urlparse(url)
    return parsed.hostname


def download_data(url):
    try:
        response = requests.get(url=url, headers={'User-Agent': ua.getEdge['useragent']}, stream=True)
        if response.ok:
            return response.content
    except Exception as err:
        print(f'Other error occurred: {err}')


def get_html_by_requests(url):
    import requests
    try:
        r = requests.get(url, headers={'User-Agent': ua.edge})
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text, r.url
    except Exception as e:
        print("Loading took too much time!", e)
        return None, None


def get_html_by_selenium(url, driver):
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print(f"{url}:Page is ready!")
        document = driver.execute_script("return document.documentElement.outerHTML")
        current_url = driver.current_url
        driver.close()
        # print(document)
        return document, current_url
    except Exception as e:
        print("Loading took too much time!", e)
        driver.close()
        return None, None


def get_icon_items(html, base_url):
    icons = []
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select('head link')
        for link in links:
            rel = link.get('rel', None)
            rel = ''.join(rel) if isinstance(rel, list) else rel
            if rel and 'icon' in rel:
                href = link.get('href', None)
                if href:
                    base_url_protocol = urlparse(base_url).scheme
                    if href.startswith('//'):
                        href = f'{base_url_protocol}:{href}'
                    if is_relative_url(url=href):
                        href = urljoin(base_url, href)
                    icons.append(Icon(target=href))
    if len(icons) == 0:
        # 插入 favicon.ico
        favicon_ico = Icon(target=f'{base_url}/favicon.ico')
        icons.append(favicon_ico)

    return icons


def check_value_type(value):
    if "data:image" in value:
        return "Base64 Image"
    elif "http" in value or value.startswith("//"):
        # 有些网站的图标地址是以 // 开头的,来自适应协议
        return "HTTP URL"
    else:
        return "Unknown Type"


class Icon:

    def __init__(self, target):
        self.target = target
        self.extension = None
        self.data = None

    def build(self):
        # 构建对象

        value_type = check_value_type(self.target)

        if value_type == 'Base64 Image':
            base64_data = self.target.split(',')[1]
            img_data = base64.b64decode(base64_data)
        elif value_type == 'HTTP URL':
            img_data = download_data(self.target)
            if img_data is None:
                return None
        else:
            return None
        data_type = magic.from_buffer(img_data, mime=True)
        file_type, extension_name = data_type.split('/')

        if file_type != 'image':
            return None

        if extension_name == 'x-icon':
            extension_name = 'ico'

        if extension_name == 'svg+xml':
            extension_name = 'svg'

        self.extension = extension_name
        self.data = img_data

    def __str__(self):
        return f'Icon: extension{self.extension} {self.target}'

    def save(self, save_dir, save_name=None):
        """
        保存图标
        :param save_dir: 保存目录
        :param save_name: 保存名称,无需后缀
        :return:
        """
        if self.data is None:
            return None

        os.makedirs(save_dir, exist_ok=True)
        if save_name is None:
            save_name = f'{len(os.listdir(save_dir))}'
        with open(f'{save_dir}/{save_name}.{self.extension}', 'wb') as f:
            f.write(self.data)


def _get_url_html(url, req_html_method='selenium', driver=None):
    """

    获取网页内容
    :param url: 网页地址
    :return:
    """
    if req_html_method == 'requests':
        html, current_url = get_html_by_requests(url)
    else:
        assert driver is not None
        html, current_url = get_html_by_selenium(url, driver)
    return html, current_url


def get_icons(url, html=None, req_html_method='selenium', selenium_driver=None) -> List[Icon]:
    """
    获取网页图标
    :param req_html_method: 或取网页内容的方法，requests 或 selenium，默认 selenium
    :param selenium_driver: 默认使用 selenium 获取网页内容，但是需要传入 selenium driver 对像
    :param url: 网页地址
    :param html: 网页内容
    :return: 返回图标对像列表
    """

    if html is None:
        html, url = _get_url_html(url, req_html_method, selenium_driver)
    base_url = get_base_url(url)
    icon_items = get_icon_items(html, base_url)

    for icon in icon_items:
        icon.build()  # 构建图标对像

    return icon_items

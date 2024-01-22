import os

from geticon import get_icons, get_hostname
from selenium import webdriver

# 设置代理
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'


def get_driver():
    # 设置 selenium
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # 使用无头模式
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("proxy-server=socks5://127.0.0.1:7890")
    return webdriver.Chrome(options=chrome_options)


if __name__ == '__main__':
    sites = [
        'https://www.baidu.com/',
        'https://www.github.com/',
        'https://www.google.com/',
        'https://www.bilibili.com/',
        'https://www.zhihu.com/',
        'https://www.taobao.com/',
        'https://www.jd.com/',
        'https://www.qq.com/',
        'https://www.sina.com.cn/',
        'https://www.weibo.com/',
        'https://www.sohu.com/',
        'https://www.tmall.com/',
        'https://www.163.com/'
    ]

    down_items = []
    save_dir = './icons'

    for site in sites:
        save_folder = get_hostname(site)
        url = site
        down_items.append((url, save_folder))

    for url, save_folder in down_items:
        icons = get_icons(url, req_html_method='selenium', selenium_driver=get_driver())
        for icon in icons:
            icon.save(save_dir=f'{save_dir}/{save_folder}')

    # 检查文件夹是否下载完成
    for _, save_folder in down_items:
        print(f'{save_dir}/{save_folder} 下载完成')
        print(f'文件数量：{len(os.listdir(f"{save_dir}/{save_folder}"))}')
        print()

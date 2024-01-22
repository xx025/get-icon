# get-icon

以极高的成功率，获取网站的favicon/icon 或 apple-touch-icon图标，支持常见的web图片类型


## 安装

```bash
pip install git+https://github.com/xx025/get-icon.git
```

## 使用案例

```python
from selenium import webdriver

from geticon import get_icons


def get_driver():
    # 设置 selenium
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # 使用无头模式
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("proxy-server=socks5://127.0.0.1:7890")
    return webdriver.Chrome(options=chrome_options)


url = 'https://github.com/'
icons = get_icons(url, req_html_method='selenium', selenium_driver=get_driver())

for index in range(len(icons)):
    icon = icons[index]
    icon.save(save_dir=f'./icon', save_name=f'{index}')
```









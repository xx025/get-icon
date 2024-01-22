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

### 说明

它的工作原理是首先获取网页的html 然后找出所有的icon链接，然后下载icon，最后使用python-magic判断icon的类型，如果是图片类型则保存

程序可以自动获取html，也可以手动提供 html；我们提供了两种获取网页html的方法，一种是使用 selenium，一种是使用 requests


#### 1. 使用 selenium

使用 selenium 需要提供一个 selenium 的 webdriver对象，如果你不知道如何使用 selenium，可以参考 https://selenium-python.readthedocs.io/installation.html

```python
from geticon import get_icons

url = 'https://github.com/'
web_driver=None # 你需要提供一个 selenium 的 webdriver对象
icons = get_icons(url, req_html_method='selenium', selenium_driver=web_driver)

```

#### 2. 使用 requests

使用 requests 方式面对反爬虫的网站时，可能会出现获取不到html的情况，推荐使用 selenium
但是你也可以自行使用其他办法获取html，然后使用自定义的html方式获取icon，见第三种方式

```python
from geticon import get_icons

url = 'https://github.com/'
icons = get_icons(url, req_html_method='requests')
```

#### 3. 使用自定义的html

```python
from geticon import get_icons

url = 'https://github.com/'
html = '<html>...</html>'
icons = get_icons(url, html=html)
```

### 返回的 Icon 对象

```python
from geticon import Icon
icons=[Icon(...),Icon(...),...]

icon=icons[0]

icon.target # icon的url 或 base64 内容，来自于网页的html
icon.data # icon的二进制内容
icon.extension # icon的类型,扩展名，例如 png jpg ico 等 
# 如果你不想保存icon，可以直接使用 icon.data 和 icon.extension 

# 如果你想保存icon，可以使用
icon.save(save_dir='./icon', save_name='1') # 保存icon, save_dir 为保存目录，save_name 为保存文件名
# 如果你不提供save_name, 则sve_name 为 目标文件夹内的文件数量 存储为 0.png 1.png 2.png ... 
```


---

**其他问题**

在Windows上使用 python-magic 往往会遇到一些问题，可以查看 https://github.com/ahupp/python-magic/issues/293 解决

此处的建议，如果在windwos 安装出现问题，先尝试卸载 python-maigc 和 python-magic-bin, 然后重新依次安装 python-maigc 和 python-magic-bin
```shell
pip uninstall python-magic python-magic-bin
pip install python-magic
pip install python-magic-bin
```









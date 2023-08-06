import setuptools
from setuptools import setup, find_packages
from pathlib import Path
setup(
    name="lzy_stock_env",
    version="1.3.9",
    author="luzhenye",
    author_email="786661074@qq.com",
    description="机器学习作业用的股票数据环境",
    #个人主页
    url="http://ursule.plus/",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages(include="lzy_stock_env*"),
    install_requires=["gym","torch"]
)
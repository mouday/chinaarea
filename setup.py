import setuptools
import os
import requests


# 将markdown格式转换为rst格式
def md_to_rst(from_file, to_file):
    r = requests.post(url='http://c.docverter.com/convert',
                      data={'to':'rst','from':'markdown'},
                      files={'input_files[]':open(from_file,'rb')})
    if r.ok:
        with open(to_file, "wb") as f:
            f.write(r.content)


md_to_rst("README.md", "README.rst")

long_description = 'Add a fallback short description here'
if os.path.exists('README.rst'):
    long_description = open('README.rst', encoding="utf-8").read()

setuptools.setup(
    name="chinaarea",
    version="0.0.5",
    author="Peng Shiyu",
    license = 'MIT License',
    author_email="pengshiyuyx@gmail.com",
    description="get a china area by province, city or county",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/mouday/chinaarea",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires = ["peewee==3.3.4", "jieba==0.39"],        # 常用
    package_data = {
            # If any package contains *.txt or *.rst files, include them:
            'chinaarea': ['stats_spider/*.sqlite']
    },
)

"""
打包上传指令：
python setup.py sdist bdist_wheel

twine upload dist/*

tree /F > tree.txt
"""
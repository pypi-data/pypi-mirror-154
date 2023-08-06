# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 1:28
# @Author  : AI悦创
# @FileName: setup.py.py
# @Software: PyCharm
# @Blog    ：https://bornforthis.cn/
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SplitMovieAIYC",
    version="1.2.0",
    author="Bornforthis",
    author_email="bornforthis@bornforthis.cn",
    description="bornforthis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
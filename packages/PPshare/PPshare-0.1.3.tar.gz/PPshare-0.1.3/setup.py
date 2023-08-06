import os
from setuptools import setup, find_packages



with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name = "PPshare",
    version = "0.1.3",
    author="Lv Yiqing",
    author_email="344599070@qq.com",
    description = 'a package for sharing',
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license = "MIT Licence",
    classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
    ],
    package_data={"": ["*.py", "*.json", "*.pk", "*.js", "*.zip"]},
    packages =find_packages(),
    include_package_data = True,
    install_requires = ['pandas','requests','tqdm','beautifulsoup4','importlib','pathlib','pypinyin','py_mini_racer'],
    platforms = "any",
)

"""
@Time ： 2022/6/9 17:21
@Auth ： 朱晓东
@File ：setup.py
@IDE ：PyCharm

"""

import setuptools

setuptools.setup(
    name="Ecarx_writeExcel",  # 模块名称
    version="1.0",  # 当前版本
    author="zhuxiaodong",  # 作者
    author_email="zhuxiaodong45@163.com",  # 作者邮箱
    description="platform8155的包",  # 模块简介
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'pillow',
    ],
    python_requires='>=3',
)

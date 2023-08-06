#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/5 15:18
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : setup.py.py

import setuptools

__version__ = None
exec(open('scienceai/version.py').read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


tests_requires = [
    "pytest"
]

install_requires = [

]

extras_requires = {
    'test': tests_requires
}

package_data = {
        "scienceai": ["*.py","*.so"]
    }

setuptools.setup(
    name="scienceai",
    version=__version__,
    author="yizheng dai",
    author_email="387942239@qq.com",
    maintainer="yizheng dai",
    maintainer_email="387942239@qq.com",
    license='Apache 2.0',
    description="Pharmacy, medicine, chemistry and biology intersect with computers and AI ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daiyizheng/scienceai",
    keywords=["Deep learning", "Drug", "Ai", "Tool"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
    ],
    install_requires= install_requires,
    tests_require=tests_requires,
    python_requires='>=3.7',
    # package_dir={'scienceai': '__main__'},
    entry_points={
         'console_scripts': [
          'scienceai = scienceai.__main__:main'
         ]
    },
    include_package_data=True,
    package_data=package_data,
    platforms='any',
    project_urls={
            'Bug Reports': 'https://github.com/daiyizheng/scienceai/issues',
            'Source': 'https://github.com/daiyizheng/scienceai',
        }
)
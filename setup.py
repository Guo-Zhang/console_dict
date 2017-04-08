from setuptools import setup

from console_dict.config import PACKAGE_VERSION

setup(
    name='console_dict',
    version=PACKAGE_VERSION,
    packages=['console_dict'],
    install_requires=[
        'pymongo',
        'xtls',
    ],
    url='github.com/Guo-Zhang/console_dict',
    license='MIT',
    author='Guo Zhang',
    author_email='zhangguo@stu.xmu.edu.cn',
    description='Command Line Version with Jinshan Dict',
    entry_points = {
    'console_scripts': [
        'dict=console_dict:main',
        'search=console_dict.search:main',
        'review=console_dict.review:main',
    ]
    }
)

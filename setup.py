from setuptools import setup

from console_dict import PACKAGE_VERSION

setup(
    name='console_dict',
    version=PACKAGE_VERSION,
    packages=['console_dict'],
    url='github.com/Guo-Zhang/console_dict',
    license='MIT',
    author='Guo Zhang',
    author_email='zhangguo@stu.xmu.edu.cn',
    description='Command Line Jinshan Dict',
    entry_points = {
    'console_scripts': [
        'dict=console_dict:main',
    ]
    }
)

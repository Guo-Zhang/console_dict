from setuptools import setup


setup(
    name='console_dict',
    version='0.0.1.dev1',
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

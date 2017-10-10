
from setuptools import setup

setup(
    name='lmk',
    version='0.1.0',
    author='Assi Maimon',
    author_email='maimon33@gmail.com',
    license='LICENSE',
    py_modules=['lmk'],
    description='KeepAlive Notifier',
    entry_points={
        'console_scripts': [
                'lmk=lmk:lmk',
        ],
    },
    install_requires=[
        'click==6.6',
        'click-didyoumean==0.0.3',
    ]
)

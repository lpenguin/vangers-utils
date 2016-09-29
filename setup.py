from setuptools import setup

setup(
    name='vangers-utils',
    version='0.1.0',
    packages=['vangers_utils', 'vangers_utils.cli', 'vangers_utils.scb', 'vangers_utils.scb.decode',
              'vangers_utils.scb.encode', 'vangers_utils.image', 'vangers_utils.image.bmp', 'vangers_utils.image.xbm'],
    url='https://github.com/lpenguin/vangers-utils',
    license='mit',
    author='nikita prianichnikov',
    author_email='lpenguin@yandex.ru',
    description='vangers resource editor',
    requires=['yaml', 'numpy', 'PIL', 'typing'],
    entry_points={
        'console_scripts': ['vangers-utils=vangers_utils.cli.main:main'],
    }
)
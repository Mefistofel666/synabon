from setuptools import find_packages, setup


setup(
    name='synabon',
    version='0.1.0',
    description='Python tool for generating data',
    author='Kirill Duvakin',
    author_email='kbduvakin1@mts.ru',
    packages=find_packages(include=['synabon']),
    download_url="https://github.com/Mefistofel666/synabon/archive/refs/tags/v.0.1.0.tar.gz",
    install_requires=['numpy>=1.25', 'pandas>=2.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.4.2'],
    test_suite='tests',
)

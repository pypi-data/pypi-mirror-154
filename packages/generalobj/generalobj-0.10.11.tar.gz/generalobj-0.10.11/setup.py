from setuptools import setup

long_description = """Testing for
Long
Description"""

setup(name='generalobj',
    version='0.10.11',
    description='Generalobj is a package for easy form handling for general Form Objects',
    url='',
    author='Csaba Saranszky',
    author_email='alt@256.hu',
    license='GPL',
    packages=['generalobj'],
    install_requires=['XlsxWriter'],
    zip_safe=False,
    include_package_data=True,
    long_description=long_description)

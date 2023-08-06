from distutils.core import  setup
import setuptools
packages = ['pip_code']# 唯一的包名，自己取名
setup(name='pip_code',
	version='1.0',
	author='syz',
    packages=packages, 
    package_dir={'requests': 'requests'},)

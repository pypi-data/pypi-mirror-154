from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='psmathplus',
  version='0.0.1',
  description='A Simple Python Library That Contains Important Mathematics Functions',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
  url='https://github.com/PeymanSeirafi/mathplus',  
  author='Peyman Seirafi',
  author_email='seirafipeyman@yahoo.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='math', 
  packages=find_packages(),
  install_requires=[''] 
)
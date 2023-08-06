from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='olekps',
  version='1.0.0',
  description='lib olekps',
  long_description=open('README.rst').read(),
  url='',  
  author='olekps',
  author_email='olekps.official@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='olekps',
  packages=find_packages(),
  install_requires=[] 
)
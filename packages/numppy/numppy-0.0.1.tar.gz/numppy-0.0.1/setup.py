from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='numppy',
  version='0.0.1',
  description='Machine Learning algorithms',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Jack Curse',
  author_email='yoyoy25532@doerma.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Machinelearning', 
  packages=find_packages(),
  install_requires=[''] 
)
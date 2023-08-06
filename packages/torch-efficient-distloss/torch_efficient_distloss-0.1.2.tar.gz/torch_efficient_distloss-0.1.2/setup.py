from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='torch_efficient_distloss',
    packages=find_packages(),
    version='0.1.2',
    license='MIT',
    description='Efficient distortion loss with O(n) realization.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Cheng Sun',
    author_email='chengsun@gapp.nthu.edu.tw',
    url='https://github.com/sunset1995',
    #download_url='https://github.com/sunset1995/torch_efficient_distloss/archive/refs/tags/v0.1.tar.gz',
    #install_requires=[],
)


from setuptools import setup, find_packages

readme = open('README.md')

setup(
    name='httpIm',
    version='1.0.0',
    author='Sendokame',
    description='Import files via HTTP.',
    long_description_content_type='text/markdown',
    long_description=readme.read(),
    packages=(find_packages(include=['http_import']))
)
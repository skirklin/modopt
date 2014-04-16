from setuptools import setup, find_packages

setup(
    name='modopt',
    version='0.0.0',
    author='S. Kirklin',
    author_email='scott.kirklin@gmail.com',
    packages=find_packages(),
    url='http://github.com/skirklin/modopt.git',
    license='LICENSE',
    package_data = {'': ['*.yml', '*.md']},
    install_requires=[
        'numpy',
        'scipy',
        'sklearn',
        'matplotlib'
    ],
)

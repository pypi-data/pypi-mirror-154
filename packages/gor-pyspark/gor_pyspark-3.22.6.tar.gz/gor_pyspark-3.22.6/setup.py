from setuptools import setup, find_packages

setup(
    name='gor_pyspark',
    version='3.22.6',
    license='Apache',
    author="Sigmar Stefansson",
    author_email='sigmar@genuitysci.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gorpipe/gor-pyspark',
    keywords='gor spark'
)
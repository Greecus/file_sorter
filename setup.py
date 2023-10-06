from setuptools import setup, find_namespace_packages

setup(
    name='File_Sorter',
    version='0.0.1',
    description='file sorting app',
    url='https://github.com/Greecus/file_sorter',
    author='Krzysztof Jaszewski',
    author_email='krzysztofjasz2002@gmail.com',
    packages=find_namespace_packages(),
    entry_points={'console_scripts':['clean-folder = file_sorter.sort:sort']}
)
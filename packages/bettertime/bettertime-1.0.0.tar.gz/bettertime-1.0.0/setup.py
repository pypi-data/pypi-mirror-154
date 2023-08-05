from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()
 
setup(
    name='bettertime',
    version='1.0.0',
    url='https://github.com/DarkJoij/bettertime',
    license='MIT License',
    author='Dallas',
    long_description_content_type='text/markdown',    
    long_description=readme,
    description='Library converting string date expressions to seconds [int].',
    packages=['bettertime'],
    zip_safe=False
)

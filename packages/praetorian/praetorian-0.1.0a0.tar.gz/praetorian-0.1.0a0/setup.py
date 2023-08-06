from pydoc import describe
import setuptools

with open('README.md', 'r') as f:
    description = f.read()

setuptools.setup(
    name='praetorian',
    version='0.1.0a',
    author='Luzhou Zhang',
    author_email='lzhang1337@gmail.com',
    packages=['praetorian'],
    description='Praetorian is a basic Sentry wrapper in Python.',
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/ThaumielSparrow/praetorian',
    license='BSD-3-Clause',
    python_requires='>=3.6',
    install_requires=[]
)
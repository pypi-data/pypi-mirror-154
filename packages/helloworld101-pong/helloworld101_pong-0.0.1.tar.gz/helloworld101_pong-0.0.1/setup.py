from setuptools import setup, find_packages


setup(
    name='helloworld101_pong',
    version='0.0.1',
    license='MIT',
    author="Tester",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project'
)
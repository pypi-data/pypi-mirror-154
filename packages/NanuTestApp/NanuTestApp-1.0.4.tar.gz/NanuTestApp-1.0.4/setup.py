from setuptools import setup
# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='NanuTestApp',
    version='1.0.4',
    packages=['pubapp'],
    url='https://github.com/pradeep9873/',
    license='MIT',
    author='rahim',
    author_email='zenith.rahim@gmail.com',
    description='nanupubapp2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='PubApp rest realtime pub/sub and rpc service',

    install_requires=[
        'python-socketio==3.1.2',
        'tornado',
        'websocket-client',
        'pyjwt',
        'python-engineio==3.14.0'
    ],

)

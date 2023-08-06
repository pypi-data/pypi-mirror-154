from setuptools import setup
# read the contents of your README file
#from pathlib import Path

#this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

setup(
    name='NanuTestApp',
    version='1.0.6',
    packages=['pubapp'],
    url='https://github.com/pradeep9873/',
    license='MIT',
    author='rahim',
    author_email='zenith.rahim@gmail.com',
    description='nanupubapp2',
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
    ]

)

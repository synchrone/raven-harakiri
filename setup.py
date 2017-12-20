from setuptools import setup

VERSION = '0.0.2'

setup(
    name='raven-harakiri',
    description='',
    author='',
    version=VERSION,
    packages=[
        '.'
    ],
    entry_points={
        'console_scripts': [
            'raven-harakiri = raven_harakiri:main'
        ]
    },
    install_requires=[
        'raven',
    ],
    python_requires='>=2.7'
)

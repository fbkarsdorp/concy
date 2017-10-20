from setuptools import setup

setup(
    name='concy',
    version='0.0.1',
    py_modules=['concy'],
    install_requires=[
        'Click',
        'pandas>=0.2',
    ],
    entry_points='''
        [console_scripts]
        concy=concy:concordance
    ''',
)
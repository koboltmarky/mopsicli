from setuptools import setup

setup(
    name='mopsicli',
    version='0.1',
    py_modules=['mopsicli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        mopsicli=mopsicli:cli
    ''',
)

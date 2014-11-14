from setuptools import setup

setup(
    name='mopsicli',
    version='0.1',
    py_modules=['mopsicli'],
    install_requires=[
        'Click',
	'json',
	'sys',
	'requests',
	'termcolor',
	'marathon',
    ],
    entry_points='''
        [console_scripts]
        mopsicli=mopsicli:cli
    ''',
)

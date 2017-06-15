from setuptools import setup

setup(
        name='notes-txt',
        version='0.1',
        py_modules=['new_file'],
        install_requires=[
            'Click',
            ],
        entry_points='''
            [console_scripts]
            notes=notes:cli
        ''',
)

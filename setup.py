from setuptools import setup

setup(
        name='notes-md',
        version='0.1',
        py_modules=['new_file'],
        install_requires=[
            'Click',
            'colorama',
            'slugify'
            ],
        entry_points='''
            [console_scripts]
            note=notes:cli
        ''',
)

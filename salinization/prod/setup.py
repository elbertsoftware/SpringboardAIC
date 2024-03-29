from distutils.core import setup


def readme():
    """Import the README.md Markdown file and try to convert it to RST format."""
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError):
        with open('README.md') as readme_file:
            return readme_file.read()


setup(
    name = 'salinization',
    version = '0.1',
    description = 'Predicting Salinization in Mekong River Delta - Vietnam',
    long_description = readme(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    url='https://github.com/elbertsoftware/SpringboardAIC/tree/master/salinization',
    author='Elbert Software',
    author_email='kennethpham@elbertsoftware',
    license='MIT',
    packages=['salinization'],
    install_requires=[
      	'pypandoc>=1.4',
        'pytest>=5.4',
        'pytest-runner>=5.2',
        'click>=7.1'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points='''
        [console_scripts]
        salinization_analysis=salinization.command_line:salinization_analysis
    '''
)
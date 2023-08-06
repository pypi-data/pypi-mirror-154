from setuptools import find_packages, setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='deutschjozsa',
    packages=find_packages(include=['']),
    version='0.0.2',
    description='Deutsch-Jozsa Algorithm library',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Me',
    license='MIT',
    classifiers=classifiers,
    keywords='deutsch-joza',
    install_requires=[''],
)
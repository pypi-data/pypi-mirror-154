import setuptools


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


setuptools.setup(
    name = "getrandomdata",
    version="0.0.5",
    description="A random data generator.",
    long_description=open("README.txt").read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='karan kaul',
    author_email='karan.kaul@grazitti.com',
    license='MIT',
    classifiers=classifiers,
    keywords='random data generator',
    packages =setuptools.find_packages(where="src"),
    python_requires='>=3.6',
    package_dir={'':'src'}
)
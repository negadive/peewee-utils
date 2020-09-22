import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='peewee_utils',
    version='0.1',
    author="Teguh Prabowo",
    author_email="putr4.g4ul@gmail.com",
    description="peewee utility, make prefetch result to dict without query",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/negadive/prefetch_to_dict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'peewee',
    ]
 )
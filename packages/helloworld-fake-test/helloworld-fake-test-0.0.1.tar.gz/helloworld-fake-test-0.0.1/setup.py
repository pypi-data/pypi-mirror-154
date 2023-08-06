from setuptools import setup

with open('README.rst') as rm:
    long_description = rm.read()


setup(
    name="helloworld-fake-test",
    version="0.0.1",
    description="Helloworld example",
    long_description=long_description,
    url="https://github.com",
    author="Sam",
    author_email="somebuddy@gmailfoo.com",
    py_modules=["helloworld"],
    package_dir= {'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "blessings ~= 1.7"
    ],
    extras_require={
        "dev": [
            "pytest >= 3.7"
        ]
    }
)

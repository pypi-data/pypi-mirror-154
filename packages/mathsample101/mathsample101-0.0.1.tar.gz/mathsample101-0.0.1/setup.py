from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mathsample101",
    version="0.0.1",
    author="Watcharapong",
    author_email="w.wattcharapong@gmail.com",
    description="test description",
    long_description="test long description",
    long_description_content_type="text/markdown",
    url="https://github.com/username/repo.git",
    license="MIT",
    packages=find_packages(),
    package_dir={'client': 'Client'},
    install_requires=[
        'requests'
    ],
    tests_require=[
        'coverage', 'wheel', 'pytest', 'requests_mock'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha"
    ]
)
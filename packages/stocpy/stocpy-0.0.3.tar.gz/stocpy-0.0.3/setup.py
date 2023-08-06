import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="stocpy",
    version="0.0.3",
    author="haoming wang",
    author_email="wanghaoming17@163.com",
    description="probability theory, stochastic process, finance engineering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/floating15/stocpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    install_requires=[
        "numpy",
        "scipy",
    ],
    python_requires=">=3",
)

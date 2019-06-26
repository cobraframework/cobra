from setuptools import setup, find_packages

with open("README.md", "r") as _readme:
    long_description = _readme.read()

with open("requirements.txt", "r") as _requirements:
    requirements = list(map(str.strip, _requirements.read().split("\n")))[:-1]

setup(
    name="py-cobra",
    version='0.1.0',
    description='Cobra Framework is a world class development environment, testing framework and '
                'asset pipeline for blockchains using the Ethereum Virtual Machine (EVM)'
                'https://cobraframework.github.io',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author='Meheret Tesfaye',
    author_email='meherett@zoho.com',
    url='https://github.com/cobraframework/cobra',
    install_requires=requirements,
    keywords=['cobra'],
    entry_points={
        'console_scripts': ["cobra=cobra.cli.__main__:main"]
    },
    python_requires=">=3.6,<4",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)

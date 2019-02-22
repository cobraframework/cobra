from setuptools import setup

setup(
    name="Cobra",
    version='0.1.0',
    description='Cobra Framework is a world class development environment, testing framework and '
                'asset pipeline for blockchains using the Ethereum Virtual Machine (EVM), aiming '
                'to make life as a developer easier.   https://cobraframework.github.io',
    long_description='TODO',
    license='MIT',
    author='Meheret Tesfaye',
    author_email='meherett@zoho.com',
    url='https://github.com/cobraframework/cobra',
    python_requires='>=3.5,<3.7',
    packages=['cobra'],
    install_requires=[
        'pytest>=3.7.1,<4.0.0',
        'eth-tester[py-evm]>=0.1.0-beta.28,<0.2.0',
        'web3>=4.4.1,<5.0.0',
        'PyYAML>=3.13,<4.0'
    ],
    entry_points='''
    [console_scripts]
    cobra=cobra:CobraFramework
    ''',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Framework :: Pytest",
    ],
)

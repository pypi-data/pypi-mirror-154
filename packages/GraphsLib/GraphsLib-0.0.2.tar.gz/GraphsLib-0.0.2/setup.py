from setuptools import setup, find_packages

setup(
    name='GraphsLib',
    version='0.0.2',
    description='Lib for working with graphs, nodes and verges.',
    url='https://github.com/Always-prog/GraphsLib',
    author='AlwaysProg',
    author_email='always.prog@gmail.com',
    license='MIT License',
    packages=find_packages(),
    install_requires=['typing>=3.7.4.3'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
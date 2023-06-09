from setuptools import setup, find_packages

setup(
    name="ts_features",
    packages=find_packages(exclude=["notebooks", "docs"]),
    version='beta',
    author='Ivan José dos Reis Filho,
    author_email='ivan.filho@uemg.br',
    description='Module for extracting time series data components.',
    long_description_content_type='text/markdown',
    url='https://github.com/ivanfilhoreis/ts_features',
    keywords='TS features',
    classifiers=[
        'Programming Language :: Python',
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    python_requires='>=3.6',
)

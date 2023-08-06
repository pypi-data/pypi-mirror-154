from setuptools import find_namespace_packages, setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Qantio.Sdk.Public",
    version="0.3.2",
    package_dir = {'': 'src'},
    packages = find_namespace_packages(where='src', exclude=["test_functional.py"]),
    description="The official SDK to interract with qant.io time series analysis and prediction services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://qant.io",
    author="qant.io",
    author_email="support@qant.io",
    license="MIT",
    keywords="qant.io, qantio, time series, forecasting, analysis, prediction, autoML, prediction as a service.",
    classifiers=[
        "Environment :: Console",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis"],
    include_package_data=False,
    python_requires=">=3.6",
    install_requires=[
        'aiohttp'
        ,'azure-storage-blob'
        ,'boto3'
        ,'colorlog'
        ,'joblib'
        ,'msal'
        ,'opencensus'
        ,'opencensus_ext_logging'
        ,'opencensus-ext-azure'
        ,'pandas'
        ,'pandas_profiling'
        ,'pyodbc'
        ,'pyparsing'
        ,'requests'
        ,'requests_toolbelt'
        ,'setuptools'
        ,'python_slugify'
        ,'urllib3'
        ,'pyarrow'
        ,'dataclasses-json'         
        ]
)
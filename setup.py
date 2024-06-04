from setuptools import setup, find_packages

with open('_VERSION') as version_file:
    version = version_file.read().strip()

setup(
    name='Files.com',
    version=version,
    license='MIT',
    description="Python bindings for the Files.com API",
    packages = find_packages(exclude = ('tests', 'tests.*', 'doc')),
    install_requires=[
        'requests >= 2.20',
        'requests-toolbelt >= 1.0.0',
    ],
    include_package_data=True,
    package_data={
        'files_sdk': ['../_VERSION', '../README.md'],
    },
    python_requires=">=3.5",
)

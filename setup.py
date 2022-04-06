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
        'requests >= 2.20; python_version >= "3.0"',
    ],
    include_package_data=True,
    package_data={
        'files_sdk': ['../_VERSION', '../README.md'],
    },
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
)

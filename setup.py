from setuptools import setup, find_packages

setup(
    name='Files.com',
    version='0.1rc0.dev0',
    license='MIT',
    description="Python bindings for the Files.com API",
    packages = find_packages(exclude = ('tests', 'doc')),
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"',
    ],
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
)

from setuptools import find_packages, setup

# Will create package of a version mentioned in the setup.
# Please append -stg when creating package for testing.

setup(
    name='gsg-utils-stg',
    packages=find_packages(include=['gsg_utils']),
    version='0.0.6',
    description='Library that will contain all utility functions that are accessible by other services.',
    url='https://bitbucket.org/global-savings-group/pouch-utils-library/src/master/',
    author='Pouch-devs',
    license='Pouch',
    install_requires=[
        'requests',
        'boto3'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    test_suite='tests',
)

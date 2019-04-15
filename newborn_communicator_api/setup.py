from setuptools import setup

setup(
    name='newborn_communicator_api',
    packages=['newborn_communicator_api'],
    include_package_data=True,
    install_requires=[
        'flask', 'requests'
    ],
)

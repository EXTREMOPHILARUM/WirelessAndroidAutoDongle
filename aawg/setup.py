from setuptools import setup, find_packages

setup(
    name='aawg',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'dbus-python',  # python-dbus
        'PyGObject',    # python-gobject
        'protobuf'      # python-protobuf
    ],
    entry_points={
        'console_scripts': [
            'aawgd = aawg.aawgd:main'
        ]
    }
)

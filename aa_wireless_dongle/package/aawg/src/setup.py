from setuptools import setup, find_packages

setup(
    name="aawg",
    version="1.0.0",
    description="Wireless Android Auto adapter implementation",
    author="nisargjhaveri",
    packages=find_packages(),
    install_requires=[
        'dbus-python>=1.2.16',
        'PyGObject>=3.36.0',  # For GLib
        'protobuf>=3.12.0',   # For protocol buffer support
    ],
    entry_points={
        'console_scripts': [
            'aawgd=aawgd:main',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: System :: Hardware',
    ],
)

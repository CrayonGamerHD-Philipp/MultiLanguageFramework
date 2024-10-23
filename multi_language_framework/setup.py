from setuptools import setup, find_packages

setup(
    name='multi_language_framework',
    version='1.0',
    packages=find_packages(),
    install_requires=['pyyaml'],
    include_package_data=True,
    description='A Python framework for multi-language message support',
    author='Philipp Hethey',
    author_email='info@hethey-bremen.de',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

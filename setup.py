import os.path
from pip.req import parse_requirements
from setuptools import setup, find_packages

setup(
    name='muto-client',
    version='0.2.5',
    description='muto is a client/server system for cloud-based image manipulation in Django projects',
    author='Philipp Bosch',
    author_email='hello+muto-client@pb.io',
    url='http://github.com/philippbosch/muto-client',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    test_suite='tests',
    install_requires=[str(ir.req) for ir in parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'))]
)

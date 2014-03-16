from setuptools import setup, find_packages

setup(
    name='muto-client',
    version='0.2',
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
)

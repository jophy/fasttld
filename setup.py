from setuptools import setup

import sys
import os

version = '0.2.1'


def test_suite():
    try:
        import unittest2
        unittest = unittest2
    except:
        import unittest

    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='maintest.py')
    return test_suite

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("git tag v%s" % (version))
    os.system("git push --tags")
    print("All Done!")
    sys.exit()


setup(
    name='fasttld',
    version=version,
    packages=['fasttld'],
    url='https://github.com/jophy/fasttld',
    license='GPL',
    author='Jophy',
    author_email='jophy.tsui@gmail.com',
    description='Python high performance TLD extract module based on a compressed trie with builtin python dict.',
    include_package_data=True,
    zip_safe=False,
    install_requires=['idna', 'setuptools'],
    test_suite='setup.test_suite',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
                 ],
)

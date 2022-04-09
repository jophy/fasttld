import subprocess
import sys

from setuptools import setup

version = 'v0.2.2'


def test_suite():
    try:
        import unittest2
        unittest = unittest2
    except Exception:
        import unittest

    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='maintest.py')
    return test_suite


if sys.argv[-1] == 'publish':
    subprocess.call(["python", "setup.py", "sdist", "upload"])
    subprocess.call(["git", "tag", version])
    subprocess.call(["git", "push", "--tags"])
    print("All Done!")
    sys.exit()


setup(
    name='fasttld',
    version=version[1:],
    packages=['fasttld'],
    url='https://github.com/jophy/fasttld',
    license='MIT',
    author='Jophy',
    author_email='jophy.tsui@gmail.com',
    description='High performance TLD extraction module based on the compressed trie data '
                'structure implemented with the builtin python dict().',
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
                 ],
)

from setuptools import setup

setup(
    name='fasttld',
    version='0.1',
    packages=['fasttld'],
    url='https://github.com/jophy/FastTLDExtract',
    license='GPL',
    author='Jophy',
    author_email='jophy.tsui@gmail.com',
    description='Python high performance TLD extract module based on a compressed trie with builtin python dict.',
    include_package_data=True,
    zip_safe=False,
    install_requires=['idna'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
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

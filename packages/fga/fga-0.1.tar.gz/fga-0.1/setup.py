from setuptools import setup

setup(name='fga',
    version='0.1',
    description='FGA consists of tools that can stack films ontop of atom slabs such that the strain in non-pseudomorphic, periodic overlayer films is minimized.',
    url="https://github.itap.purdue.edu/GreeleyGroup/fga",
    author='Kaustubh Sawant',
    author_email="sawantk@purdue.edu",
    python_requires=">=3.00",
    packages=['fga'],
    license='LGPLv2.1+',
    scripts=['bin/run_fga'],
    zip_safe=False)

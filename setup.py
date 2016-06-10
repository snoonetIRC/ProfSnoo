from setuptools import setup, find_packages

requires = []

setup(
    name='ProfSnoo',
    version='1.0.0',
    author="Evan Snoonet",
    author_email="evan@snoonet.org",
    creator="Evan",
    package_dir={'': 'src'},
    packages=find_packages("src"),
    install_requires=requires,
    zip_safe=False,
)

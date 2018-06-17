from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name="mock_aerohive",
      version="0.0.1",
      description="A mock SSH server emulating Aerohive devices",
      long_description=readme(),
      url="https://github.com/pencot/mock_aerohive",
      author="Ryan Leonard",
      license="MIT",
      packages="mock_aerohive",
      install_requires=[
        "mockssh >=1.4.5,<2"
      ],
      include_package_data=True)

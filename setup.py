from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = []
with open('requirements.txt', 'r') as f:
  for line in f:
    if line.strip():
      install_requires.append(line.strip())

setup (
  name='lt-norm-stress-dataset-gen',
  version='0.0.1',
  long_description=long_description,
  long_description_content_type="text/markdown",
  zip_safe=False,
  packages=find_packages(),
  install_requires=install_requires
)
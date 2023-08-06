import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='bregmanet',
      version='0.1',
      author='Jordan Frecon',
      author_email='jordan.frecon@gmail.com',
      description='Bregman Neural Network',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/JordanFrecon/bregmanet',
      license='MIT',
      package_dir={"": "src"},
      packages=setuptools.find_packages(where="src"),
      python_requires=">=3.6",
      )


from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='xwind',
      version='1.0.9',
      description='xwind core functions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='XWind',
      classifiers=[
              "Programming Language :: Python :: 3",
              "Operating System :: OS Independent",
          ],
      install_requires=['numpy', 'pandas>=1.3.0', 'scipy', 'openpyxl', 'chardet', 'charset-normalizer', 'simplekml',
                        'Deprecated'],
      packages=find_packages(exclude=['test1', 'build', 'dist']),
      python_requires=">=3.9"
      )

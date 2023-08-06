from setuptools import setup, Extension

setup(
    name="native-sum-lib",
    version="0.0.1",
    description="cpp method",
    author="Tomasz Gorniak",
    ext_modules=[Extension('native-sum-lib', ['library.c'])]
)

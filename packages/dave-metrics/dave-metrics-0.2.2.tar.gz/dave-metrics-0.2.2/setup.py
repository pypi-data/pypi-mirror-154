from setuptools import find_packages, setup

setup(
    name="dave-metrics",
    version="0.2.2",
    install_requires=[],
    extras_require={"test": []},
    package_data={"dave-metrics": ["py.typed"]},
    packages=find_packages(include=["metrics", "metrics.**"]),
)




from setuptools import setup, find_packages

setup(
    name="payjoy-disable-tool",
    version="1.0.0",
    author="bhuda1022-eng",
    description="Command-line tool to disable or toggle Payjoy functionality",
    url="https://github.com/bhuda1022-eng/payjoy-disable-tool",
    py_modules=["payjoy_disable"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "payjoy-disable=payjoy_disable:main",
        ],
    },
)

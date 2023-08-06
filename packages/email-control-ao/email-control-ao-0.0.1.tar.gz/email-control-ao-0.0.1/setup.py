from setuptools import setup, find_packages

setup(
    name="email-control-ao",
    version="0.0.1",
    author="wangziling100",
    author_email="wangziling100@163.com",
    description="Exposed interface tool for email service",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
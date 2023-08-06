from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="tf_cli",
    version="0.0.1",
    description="This contains a CLI for AWS terraform",
    author="Rooklyn Kline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rkline2/tf_cli",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={'':['scripts/*']},
    include_package_data=True,
    install_requires=install_requires,
    entry_points = {
        'console_scripts':[
            'tf = tf.cli:main',
        ],
    },
    python_requires=">=3.7",
    extras_require={
        "dev": [
            "pytest==6.2.5",
            "wheel==0.37.0",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
    ]
)

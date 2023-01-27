import sys
import os
import os.path
from setuptools import setup, find_packages  # type: ignore

local_link = os.path.join(os.getcwd(), "external", "autonity.py#egg=autonity.py")
sys.stderr.write(f"local_link={local_link}\n")


setup(
    name="autcli",
    version="0.1.1",
    authors=[
        {"name": "Robert Sams", "email": "rs@clearmatics.com"},
        {"name": "Duncan Tebbs", "email": "duncan.tebbs@clearmatics.com"},
    ],
    description="A command-line RPC client for Autonity",
    packages=find_packages(exclude=["tests", "external"]),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        f"autonity.py @ file://{local_link}",
        "click==8.1.3",
    ],
    extras_require={
        "dev": [
            "mypy==0.982",
            "pylint==2.15.4",
            "flake8==5.0.4",
            "black==22.12.0",
        ],
    },
    tests_require=["unittest"],
    entry_points={"console_scripts": ["aut=autcli.__main__:aut"]},
    project_urls={
        "Homepage": "http://github.com/clearmatics/autcli",
    },
)

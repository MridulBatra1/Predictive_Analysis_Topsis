from setuptools import setup, find_packages

setup(
    name="topsis-mridul-102317082",   # MUST BE UNIQUE (lowercase)
    version="1.0.0",
    author="Mridul Batra",
    author_email="mridulbatra2005@gmail.com",
    description="TOPSIS implementation with CLI and Web App",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "flask"
    ],
    entry_points={
        'console_scripts': [
            'topsis=topsis.cli:main'
        ]
    },
    python_requires='>=3.6',
)

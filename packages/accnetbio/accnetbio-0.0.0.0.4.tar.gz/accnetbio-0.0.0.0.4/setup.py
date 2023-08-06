from setuptools import setup, find_packages

setup(
    name="accnetbio",
    # version="0.0.6",
    version="0.0.0.0.4",
    keywords=("pip", "accnetbio"),
    description="acc network biology",
    long_description="accelerate network biology",
    license="MIT",

    url="https://github.com/2003100127",
    author="Jianfeng Sun",
    author_email="jianfeng.sun@ndorms.ox.ac.uk",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    python_requires='>3.6',
    install_requires=[
        'pandas==1.3.5',
        'numpy==1.19.5',
        'biopython==1.79',
        'pyfiglet==0.8.post1',
    ],
    entry_points={
        'console_scripts': [
            'accnetbio=accnetbio.Main:main',
        ],
    }
)
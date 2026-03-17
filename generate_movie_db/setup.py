from setuptools import setup, find_packages

setup(
    name="generate_movie_db",
    version="1.0.0",
    author="Gal",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["os", "sqlite3", "gzip", "urllib", "heapdict"],
)

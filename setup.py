from setuptools import find_packages, setup


setup(
    name="cognition-store",
    version="0.4.0",
    description="Local-first evidence, memory, dashboard, and decision record system",
    packages=find_packages(include=["cognition_store", "cognition_store.*"]),
    python_requires=">=3.10",
    extras_require={"dev": ["pytest>=8.0"]},
    entry_points={"console_scripts": ["cognition-store=cognition_store.cli:main"]},
)

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="journalizeio",
    version="0.0.3",
    author="Journalize.io",
    author_email="support@journalize.io",
    description="Client library for journalize.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/journalize-io/journalize-python",
    project_urls={
        "Homepage": "https://www.journalize.io",
        "Source Code": "https://github.com/journalize-io/journalize-python",
    },
    packages=['journalizeio'],
    python_requires=">=3.6",
    install_requires=['requests']
)
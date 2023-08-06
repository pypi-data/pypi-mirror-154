# Journalize Python Library

The Journalize Python Library provides access to the Journalize API from
applicaitons written in the Python language.

## Installation

```sh
pip3 install journalizeio
```

## Usage

```python
from journalizeio import JournalizeClient

# Initialize client
client = JournalizeClient("your_api_key")

# Test connectivity and API key
client.ping()

# Record financial transaction
client.record(
    amount=15.00,
    tags={"Account": "Revenue", "Order": "1123"}
)
```

## Manual Build

1. Increment version in setup.py, client.py, update changelog

2. Perform build

```sh
python3 -m build
```

3. Uplaod to test pypi. Username `__token__` password is API Key. 
   
```
python3 -m twine upload --repository testpypi dist/*
```

4. Uplaod to pypi. Username `__token__` password is API Key. 
   
```
python3 -m twine upload dist/*
```
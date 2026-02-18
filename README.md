# Bunnyhop (New)

A modern, pythonic client for Bunny.net API unofficial library.

## Features
- **Modern**: Uses `pydantic` for data validation and `httpx` for HTTP requests.
- **Simple**: Easy to use `BunnyClient` interface.
- **Type Safe**: Full type hinting support.

# Why did I write this library?

1. I wrote this library because I wanted to make it easier to use the Bunny.net API.
2. Why not? :D

Not: Maybe I can add this library to PyPI.

# Contact Information

| Gmail: jdhdudhudkd603@gmail.com |
| Discord: erdemgalibov |

## Installation

```bash
pip install httpx pydantic
```

## Usage

### Initialization

```python
from bunnyhop import BunnyClient

client = BunnyClient(api_key="YOUR_API_KEY")
```

### Pull Zones

```python
# List all zones
zones = client.zone.list()
for zone in zones:
    print(zone.name, zone.id)

# Create a zone
new_zone = client.zone.create(name="my-zone", origin_url="https://example.com")

# Get a zone
zone = client.zone.get(new_zone.id)

# Purge Cache
client.zone.purge(zone.id)
```

### Storage

```python
# List Storage Zones
storage_zones = client.storage.list()

# Get a specific storage zone
store = client.storage.get(12345)

# Upload a file
with open("test.jpg", "rb") as f:
    client.storage.upload_file(
        zone=store,
        path="images/",
        filename="test.jpg",
        file_content=f.read()
    )

# Download a file
content = client.storage.download_file(
    zone=store,
    path="images/",
    filename="test.jpg"
)
```

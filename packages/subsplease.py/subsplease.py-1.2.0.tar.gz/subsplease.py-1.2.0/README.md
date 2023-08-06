# subsplease.py 
A simple and asynchronous wrapper for SubsPlease.

# Installation
```
pip install subsplease.py
```

# Implementation
```python
from subsplease import SubsPlease

client = SubsPlease()

async def save_new_releases():
    releases = await client.get_latest_magnet()
    with open("magnet.txt", "w") as file:
        file.writelines(f"{release.title}: {release.link}\n" for release in releases)
```


# Libvirt Chores

Periodically dump libvirt XML into `/data`

- `domain` (VMs)

- `network`

- `storage`

## Usage

```yaml
---
version: "3.7"

services:
  libvirt-chores:
    restart: always
    image: msjpq/libvirt-chores:latest
    environment:
      TZ:
    volumes:
      - /var/run/libvirt/libvirt-sock-ro:/var/run/libvirt/libvirt-sock-ro:ro
      - ./data:/data
```

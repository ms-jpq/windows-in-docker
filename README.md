# Libvirt Chores

Periodically dump libvirt `domain` (VMs), `network` and `storage` XML into `/data`

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

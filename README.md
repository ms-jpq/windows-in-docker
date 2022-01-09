# [Libvirt Chores](https://ms-jpq.github.io/libvirt-chores)

## Chores

### Backup XML

Periodically dump libvirt XML into `/data/backup`

- `domain` (VMs)

- `network`

- `storage`

### Download Windows Drivers

Periodically dump latest virtio-win.iso into `/data/downloads`

[From latest stable release](https://github.com/virtio-win/virtio-win-pkg-scripts)

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

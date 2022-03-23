# [Libvirt Chores](https://ms-jpq.github.io/libvirt-chores)

## Chores

### Download Windows Drivers

Periodically dump latest virtio-win.iso into `/data`

[From latest stable release](https://github.com/virtio-win/virtio-win-pkg-scripts)

### Virt Manager

## Usage

```yaml
---
version: "3.9"

services:
  libvirt:
    restart: always
    image: msjpq/libvirt-chores:latest
    security_opt:
      - apparmor=unconfined
    environment:
      TZ:
    ports:
      - 80:8080
    volumes:
      - /var/run/libvirt/libvirt-sock:/var/run/libvirt/libvirt-sock:ro
      - ./data:/data
```

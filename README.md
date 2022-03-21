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
    environment:
      TZ:
    ports:
      - 80:80
    volumes:
      - /var/run/libvirt/libvirt-admin-sock:/var/run/libvirt/libvirt-admin-sock:ro
      - /var/run/libvirt/libvirt-sock-ro:/var/run/libvirt/libvirt-sock-ro:ro
      - /var/run/libvirt/libvirt-sock:/var/run/libvirt/libvirt-sock:ro
      - /var/run/libvirt/virtlockd-admin-sock:/var/run/libvirt/virtlockd-admin-sock:ro
      - /var/run/libvirt/virtlockd-sock:/var/run/libvirt/virtlockd-sock:ro
      - /var/run/libvirt/virtlogd-admin-sock:/var/run/libvirt/virtlogd-admin-sock:ro
      - /var/run/libvirt/virtlogd-sock:/var/run/libvirt/virtlogd-sock:ro
      - ./data:/data
```

# Buildroot Files

This directory contains all the necessary files and folders required to build the OS image from scratch using Buildroot.

## Structure Overview

### `board/`

Contains board-specific configuration files. Currently, it supports:

* Raspberry Pi 4 (64-bit)

### `overlay/`

This folder includes the root filesystem overlay. It's used to add custom files and configurations to the final OS image.

### `Other/`

A miscellaneous folder where additional or optional files are kept — basically, anything that doesn't fit into the two categories above.

---

Everything here ties into creating a customized, bootable image with all the components needed for the system to work out of the box.


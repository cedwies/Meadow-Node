# Bitcoin\_Node

A bootable, plug-and-play image to turn your Raspberry Pi 4 or 5 into a fully functional Bitcoin full node.

## Quick Start

If you're just here to get up and running quickly — no fluff, no detours — here's what you need to do:

---

### 🧰 What you need (prerequisites)
- **Raspberry Pi 4 (x64)** with at least **4 GB RAM**, connected with a LAN cable (WLAN not supported yet)
- **SSD with 1 TB** if you want to store the full blockchain right away
  - If you just want to boot the system for now and see it running, a small USB stick (even 2 GB) will do
- **SD card** with at least **8 GB** (though 16 GB+ is better)
- A way to plug the SD card into your computer (USB adapter, built-in slot, etc.)

---

### 🚀 Flashing the Image

1. **Download the image**
   - Go to [Meadow-Node Releases](https://github.com/cedwies/Meadow-Node/releases)
   - Look for the latest version, something like `Meadow-Node-0.1.0.img.zip`
   - 
     - If you're on **Linux**, you're probably fine with `.gz` or `.xz`
     - On **Windows**, stick with the `.zip`. After downloading, extract it — you should get a `.img` file like `Meadow-Node-x.y.z.img`

2. **Download Balena Etcher**
   - Grab it from [etcher.balena.io](https://etcher.balena.io/)
   - Works on **Linux**, **macOS**, and **Windows**

3. **Plug in your SD card**
   - Use your card reader, adapter, or whatever you've got

4. **Open Balena Etcher**
   - Click **"Flash from file"** and select the `.img` you extracted earlier
   - Click **"Select target"** and pick your SD card
   - Hit **"Flash"** — you might have to enter your system password

5. **Wait a bit**
   - Once Etcher says it's done, safely eject the SD card

---

### 💡 Boot it up

1. Stick the SD card into your **Raspberry Pi 4 (x64)**
2. Conncect the SSD/USB into a USB-Port of your **Raspberry Pi 4 (x64)**
3. Make sure, your  **Raspberry Pi 4 (x64)** is connected by a LAN cable.
4. Power it on
5. Wait **2–5 minutes** for it to initialize everything on first boot

Then, from a device on the same network (laptop, etc.), open your browser and go to:

**[http://meadow.local](http://meadow.local)**

If that doesn't load, try using your Pi's IP address directly instead.

---

Boom — you're in. Welcome to Meadow.

## Status

Currently, this project is in an early but working state. You can download the ISO, flash it, boot it on your Raspberry Pi, and install & run Bitcoin Core.

However, it's not yet a full-featured node setup. Components like Electrs or Mempool aren't included in the build yet — those are planned.

In short: the basics work, but it's still a work in progress.

## Verifying Check-Sum

Don't trust - verify. To see the guide on how to verify the Check-Sums, see doc/

## Motivation

This project started out of a mix of curiosity and a desire to build a simple, user-friendly Bitcoin node — especially for people who aren't deep into tech.

The main goal: make it easy for anyone to run a Bitcoin full node. Whether you're looking to support the Bitcoin network, gain full sovereignty over your transactions, or just want to tinker around, this setup is meant to make that path smooth.

Yes, there are existing projects like UmbrelOS and CitadelOS, and they're great. But they’re also multi-purpose platforms — think personal file servers, app ecosystems, and more. That extra functionality, while cool, makes the OS more bloated than it needs to be if your only goal is running a Bitcoin node.

Also, those platforms rely heavily on Docker, which adds internal complexity and can be a bit fragile — especially in environments with unreliable power (think: sudden power cuts).

### What This Project Tries to Offer

A minimal, purpose-built OS designed specifically for:

* Running **Bitcoin Core**
* Running **Electrs** (an efficient Electrum server)
* Running a **personal Mempool**

No unnecessary extras. No containers. Just a lean, focused system built for Bitcoin, with the simplicity and resilience that non-nerds (and nerds too, honestly) will appreciate.

In the future, I am to add more safety for e.g. power cuts. 3 power cuts while using UmbrelOS (which damaged the OS beyond repair, was actually what has gotten me into this project - pff.



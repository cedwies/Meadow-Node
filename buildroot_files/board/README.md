# Board Configurations

This folder holds board-specific configurations used by Buildroot to generate OS images tailored for different hardware.

Currently, it includes:
- Raspberry Pi 4 (64-bit)

You can expand this to include support for:
- Raspberry Pi 4 (32-bit)
- Raspberry Pi 5 (both 32/64-bit)
- Other ARM boards or even different CPU architectures as needed

Each subdirectory should contain the relevant configuration files for its specific board.

If you're adding a new board, just follow the structure of the existing ones and plug in your config tweaks.

Note: The actual build scripts aren't inside the board subdirectories — they live at the top level of the repository.

For example: build_raspberrypi4_64.sh


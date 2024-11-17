# `board` Directory

The `board` directory contains configuration files and scripts specific to different hardware boards supported by the Wireless Android Auto Dongle project. These files are used to customize the build process and runtime behavior for each supported board.

## Contents

### `common`

The `common` directory contains files that are common across all supported boards. These files include kernel configuration, root filesystem overlay, and other common scripts.

#### `kernel.config`

The `kernel.config` file contains kernel configuration options that are applied to all supported boards. It includes options for USB gadget support, Bluetooth configuration, and kernel debugging options.

#### `rootfs_overlay`

The `rootfs_overlay` directory contains files that are overlaid onto the root filesystem during the build process. These files include configuration files for various services, initialization scripts, and other necessary files.

### `raspberrypi`

The `raspberrypi` directory contains configuration files and scripts specific to Raspberry Pi boards. It includes files for boot configuration, device tree overlays, and other board-specific settings.

#### `cmdline.txt`

The `cmdline.txt` file contains the kernel command line parameters for Raspberry Pi boards. It specifies the root filesystem location and other boot parameters.

#### `config.txt`

The `config.txt` file contains configuration options for the Raspberry Pi firmware. It includes options for enabling USB gadget mode, setting GPU memory, and other board-specific settings.

#### `genimage.cfg.in`

The `genimage.cfg.in` file is used to generate the final SD card image for Raspberry Pi boards. It specifies the partition layout and includes the necessary files for booting the board.

#### `post-build.sh`

The `post-build.sh` script is executed after the build process is complete. It performs additional setup tasks specific to Raspberry Pi boards.

#### `post-image.sh`

The `post-image.sh` script is executed after the SD card image is generated. It performs additional setup tasks specific to Raspberry Pi boards.

#### `rootfs_overlay`

The `rootfs_overlay` directory contains files that are overlaid onto the root filesystem during the build process. These files include configuration files for various services, initialization scripts, and other necessary files.

### `raspberrypi4`

The `raspberrypi4` directory contains configuration files and scripts specific to Raspberry Pi 4 boards. It includes files for boot configuration, device tree overlays, and other board-specific settings.

#### `rootfs_overlay`

The `rootfs_overlay` directory contains files that are overlaid onto the root filesystem during the build process. These files include configuration files for various services, initialization scripts, and other necessary files.

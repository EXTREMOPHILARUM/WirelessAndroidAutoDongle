################################################################################
#
# aawg
#
################################################################################

AAWG_VERSION = 1.0
AAWG_SITE = $(BR2_EXTERNAL_AA_WIRELESS_DONGLE_PATH)/package/aawg/src
AAWG_SITE_METHOD = local
AAWG_SETUP_TYPE = setuptools
AAWG_DEPENDENCIES = python3 python-dbus python-gobject python-protobuf host-python-protobuf host-python-grpcio-tools

define AAWG_GENERATE_PROTO
	$(HOST_DIR)/bin/python -m grpc_tools.protoc \
		--python_out=$(@D) \
		--proto_path=$(@D)/proto \
		$(@D)/proto/*.proto
endef

AAWG_PRE_BUILD_HOOKS += AAWG_GENERATE_PROTO

# Init scripts are now handled through board/common/rootfs_overlay
# No need for AAWG_INSTALL_INIT_SYSV or AAWG_INSTALL_INIT_SYSTEMD

$(eval $(python-package))

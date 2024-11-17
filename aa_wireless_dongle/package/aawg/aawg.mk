################################################################################
#
# aawg
#
################################################################################

AAWG_VERSION = 1.0
AAWG_SITE = $(BR2_EXTERNAL_AA_WIRELESS_DONGLE_PATH)/aawg
AAWG_SITE_METHOD = local
AAWG_SETUP_TYPE = setuptools
AAWG_DEPENDENCIES = python3 python-dbus python-gobject python-protobuf host-python-protobuf

define AAWG_GENERATE_PROTO
	$(HOST_DIR)/bin/protoc \
		--python_out=$(@D) \
		--proto_path=$(@D)/proto \
		$(@D)/proto/*.proto
endef

AAWG_PRE_BUILD_HOOKS += AAWG_GENERATE_PROTO

$(eval $(python-package))

OBS_PROJECT := EA4-experimental
OBS_PACKAGE := ea-modsec30-connector-nginx
DISABLE_BUILD = repository=CentOS_6.5_standard repository=CentOS_9
include $(EATOOLS_BUILD_DIR)obs.mk

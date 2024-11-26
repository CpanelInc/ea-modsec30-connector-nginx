#!/bin/bash

source debian/vars.sh

set -x 

rm -rf $DEB_INSTALL_ROOT
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-modsec30-connector-nginx
mkdir -p $DEB_INSTALL_ROOT/etc/nginx/conf.d/modules
mkdir -p $DEB_INSTALL_ROOT/etc/nginx/conf.d/modsec_vendor_configs
mkdir -p $DEB_INSTALL_ROOT/var/log/nginx/modsec30_audit
/bin/cp -rf ./* $DEB_INSTALL_ROOT/opt/cpanel/ea-modsec30-connector-nginx
/bin/cp -rf $SOURCE1 $DEB_INSTALL_ROOT/etc/nginx/conf.d/modules/ngx_http_modsecurity_module.conf
mkdir -p $DEB_INSTALL_ROOT/etc/nginx/conf.d/modsec
mkdir -p $DEB_INSTALL_ROOT/etc/nginx/ea-nginx/config-scripts/global/
/bin/cp -rf $SOURCE2 $DEB_INSTALL_ROOT/etc/nginx/conf.d/modsec30.conf
/bin/cp -rf $SOURCE3 $DEB_INSTALL_ROOT/etc/nginx/conf.d/modsec/modsec30.cpanel.conf
/bin/cp -rf $SOURCE4 $DEB_INSTALL_ROOT/etc/nginx/ea-nginx/config-scripts/global/modsec30.cpanel.conf-generate
chmod a+x $DEB_INSTALL_ROOT/etc/nginx/ea-nginx/config-scripts/global/modsec30.cpanel.conf-generate
/bin/cp -rf $SOURCE5 $DEB_INSTALL_ROOT/etc/nginx/ea-nginx/modsec30.cpanel.conf.tt
/bin/cp -rf $SOURCE6 $DEB_INSTALL_ROOT/etc/nginx/conf.d/modsec/modsec30.user.conf


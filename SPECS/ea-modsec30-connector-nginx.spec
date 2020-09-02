%define debug_package %{nil}

Name: ea-modsec30-connector-nginx
Summary: NGINX connector for ModSecurity v3.0
Version: 1.0.1
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 2
Release: %{release_prefix}%{?dist}.cpanel
Vendor: cPanel, Inc.
Group: System Environment/Libraries
License: Apache v2
URL: https://github.com/SpiderLabs/ModSecurity-nginx

Source0: https://github.com/SpiderLabs/ModSecurity-nginx/archive/v%{version}.tar.gz
Source1: ngx_http_modsecurity_module.conf
Source2: modsec30.conf
Source3: modsec30.cpanel.conf
Source4: modsec30.cpanel.conf-generate
Source5: modsec30.cpanel.conf.tt
Source6: modsec30.user.conf

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReq:   no

BuildRequires: ea-modsec30

Requires: ea-modsec30 ea-nginx >= 1.19.1-9

%description

The ModSecurity-nginx connector is the connection point between
 nginx and libmodsecurity (ModSecurity v3).

%prep
%setup -q -n ModSecurity-nginx-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-modsec30-connector-nginx
mkdir -p $RPM_BUILD_ROOT/etc/nginx/conf.d/modules

mkdir -p $RPM_BUILD_ROOT/etc/nginx/conf.d/modsec_vendor_configs
mkdir -p $RPM_BUILD_ROOT/var/log/nginx/modsec30_audit

/bin/cp -rf ./* $RPM_BUILD_ROOT/opt/cpanel/ea-modsec30-connector-nginx
/bin/cp -rf %{SOURCE1} $RPM_BUILD_ROOT/etc/nginx/conf.d/modules/ngx_http_modsecurity_module.conf

mkdir -p $RPM_BUILD_ROOT/etc/nginx/conf.d/modsec
mkdir -p $RPM_BUILD_ROOT/etc/nginx/ea-nginx/config-scripts/global/
/bin/cp -rf %{SOURCE2} $RPM_BUILD_ROOT/etc/nginx/conf.d/modsec30.conf
/bin/cp -rf %{SOURCE3} $RPM_BUILD_ROOT/etc/nginx/conf.d/modsec/modsec30.cpanel.conf
/bin/cp -rf %{SOURCE4} $RPM_BUILD_ROOT/etc/nginx/ea-nginx/config-scripts/global/modsec30.cpanel.conf-generate
/bin/cp -rf %{SOURCE5} $RPM_BUILD_ROOT/etc/nginx/ea-nginx/modsec30.cpanel.conf.tt
/bin/cp -rf %{SOURCE6} $RPM_BUILD_ROOT/etc/nginx/conf.d/modsec/modsec30.user.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post

/etc/nginx/ea-nginx/config-scripts/global/modsec30.cpanel.conf-generate

%files
%defattr(-, root, root, -)
/opt/cpanel/ea-modsec30-connector-nginx
/etc/nginx/conf.d/modules/ngx_http_modsecurity_module.conf
%attr(0755 root root) %dir /etc/nginx/conf.d/modsec_vendor_configs
%attr(1733 root root) %dir /var/log/nginx/modsec30_audit

# Don't make modsec30.conf a config file, we need to ensure we own this and can fix as needed
%attr(0600,root,root) /etc/nginx/conf.d/modsec30.conf
%attr(0600,root,root) %config(noreplace) /etc/nginx/conf.d/modsec/modsec30.cpanel.conf
%attr(0755 root root) /etc/nginx/ea-nginx/config-scripts/global/modsec30.cpanel.conf-generate
/etc/nginx/ea-nginx/modsec30.cpanel.conf.tt
%attr(0600,root,root) %config(noreplace) /etc/nginx/conf.d/modsec/modsec30.user.conf

%changelog
* Wed Sep 02 2020 Daniel Muey <dan@cpanel.net> - 1.0.1-2
- ZC-7445: Several fixes to log directories

* Tue Aug 18 2020 Daniel Muey <dan@cpanel.net> - 1.0.1-1
- ZC-7366: initial release


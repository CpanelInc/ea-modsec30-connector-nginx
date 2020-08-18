%define debug_package %{nil}

Name: ea-modsec30-connector-nginx
Summary: NGINX connector for ModSecurity v3.0
Version: 1.0.1
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
Vendor: cPanel, Inc.
Group: System Environment/Libraries
License: Apache v2
URL: https://github.com/SpiderLabs/ModSecurity-nginx

Source0: https://github.com/SpiderLabs/ModSecurity-nginx/archive/v%{version}.tar.gz
Source1: ngx_http_modsecurity_module.conf

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReq:   no

BuildRequires: ea-modsec30

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

/bin/cp -rf ./* $RPM_BUILD_ROOT/opt/cpanel/ea-modsec30-connector-nginx
/bin/cp -rf %{SOURCE1} $RPM_BUILD_ROOT/etc/nginx/conf.d/modules/ngx_http_modsecurity_module.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
/opt/cpanel/ea-modsec30-connector-nginx
/etc/nginx/conf.d/modules/ngx_http_modsecurity_module.conf

%changelog
* Tue Aug 18 2020 Daniel Muey <dan@cpanel.net> - 1.0.1-1
- ZC-7366: initial release


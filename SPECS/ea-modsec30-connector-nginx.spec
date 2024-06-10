Name: ea-modsec30-connector-nginx
Summary: NGINX connector for ModSecurity v3.0
Version: 1.0.3
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 9
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
Source7: Modsec30NginxHooks.pm

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReq:   no

BuildRequires: ea-modsec30
BuildRequires: ea-nginx-ngxdev

Requires: ea-modsec30 ea-nginx >= 1.24.0-3

%description

The ModSecurity-nginx connector is the connection point between
 nginx and libmodsecurity (ModSecurity v3).

%prep
%setup -q -n ModSecurity-nginx-%{version}

%build

export MODSECURITY_LIB=/opt/cpanel/ea-modsec30/lib
export MODSECURITY_INC=/opt/cpanel/ea-modsec30/include

# You will be in ./nginx-build after this source()
#    so that configure and make etc can happen.
# We probably want to popd back when we are done in there
. /opt/cpanel/ea-nginx-ngxdev/set_NGINX_CONFIGURE_array.sh
./configure "${NGINX_CONFIGURE[@]}" --add-dynamic-module=..
make %{?_smp_mflags}
popd

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

mkdir -p $RPM_BUILD_ROOT/var/cpanel/perl5/lib
%{__install} -p %{SOURCE7} $RPM_BUILD_ROOT/var/cpanel/perl5/lib/Modsec30NginxHooks.pm

mkdir -p %{buildroot}%{_libdir}/nginx/modules
install ./nginx-build/objs/ngx_http_modsecurity_module.so %{buildroot}%{_libdir}/nginx/modules/ngx_http_modsecurity_module.so

%clean
rm -rf $RPM_BUILD_ROOT

%pre

# See ea-nginx SPEC for details
numhooks=`/usr/local/cpanel/bin/manage_hooks list 2> /dev/null | grep 'hook: Modsec30NginxHooks::' | wc -l`
if [ "$numhooks" -ge 1 ]; then
   /usr/local/cpanel/bin/manage_hooks delete module Modsec30NginxHooks
fi

%preun

# See ea-nginx SPEC for details
numhooks=`/usr/local/cpanel/bin/manage_hooks list 2> /dev/null | grep 'hook: Modsec30NginxHooks::' | wc -l`
if [ "$numhooks" -ge 1 ]; then
    /usr/local/cpanel/bin/manage_hooks delete module Modsec30NginxHooks
fi

%post

/etc/nginx/ea-nginx/config-scripts/global/modsec30.cpanel.conf-generate

%posttrans

# If the Apache connector is not installed these will be missing
#   which can cause spurious errors from ULC about not being able to open them.
# We don't want the NGINX connector to own them because then the
#   connectors could not be installed at the same time.
# If they are there and empty (or even not-empty FTM since they won't be `Include`d) they are noops.
# All of that being the case: we touch them here (and do not remove them uninstall) so that ULC will be happy.

mkdir -p /etc/apache2/conf.d/modsec
touch /etc/apache2/conf.d/modsec/modsec2.cpanel.conf
touch /etc/apache2/conf.d/modsec/modsec2.user.conf

# See ea-nginx SPEC for details
/usr/local/cpanel/bin/manage_hooks prune; /bin/true;
/usr/local/cpanel/bin/manage_hooks add module Modsec30NginxHooks

%files
%defattr(-, root, root, -)
/opt/cpanel/ea-modsec30-connector-nginx
/etc/nginx/conf.d/modules/ngx_http_modsecurity_module.conf
%attr(0755 root root) %dir /etc/nginx/conf.d/modsec_vendor_configs
%attr(1733 root root) %dir /var/log/nginx/modsec30_audit

%attr(0755, root, root) /var/cpanel/perl5/lib/Modsec30NginxHooks.pm

# Don't make modsec30.conf a config file, we need to ensure we own this and can fix as needed
%attr(0600,root,root) /etc/nginx/conf.d/modsec30.conf
%attr(0600,root,root) %config(noreplace) /etc/nginx/conf.d/modsec/modsec30.cpanel.conf
%attr(0755 root root) /etc/nginx/ea-nginx/config-scripts/global/modsec30.cpanel.conf-generate
/etc/nginx/ea-nginx/modsec30.cpanel.conf.tt
%attr(0600,root,root) %config(noreplace) /etc/nginx/conf.d/modsec/modsec30.user.conf
%attr(0755,root,root) %{_libdir}/nginx/modules/ngx_http_modsecurity_module.so

%changelog
* Mon Jun 10 2024 Cory McIntire <cory@cpanel.net> - 1.0.3-9
- EA-12203: Build against ea-nginx version v1.26.1

* Tue Apr 23 2024 Cory McIntire <cory@cpanel.net> - 1.0.3-8
- EA-12112: Build against ea-nginx version v1.26.0

* Tue Apr 16 2024 Cory McIntire <cory@cpanel.net> - 1.0.3-7
- EA-12100: Build against ea-nginx version v1.25.5

* Wed Feb 14 2024 Cory McIntire <cory@cpanel.net> - 1.0.3-6
- EA-11973: Build against ea-nginx version v1.25.4

* Thu Oct 26 2023 Cory McIntire <cory@cpanel.net> - 1.0.3-5
- EA-11772: Build against ea-nginx version v1.25.3

* Thu Aug 24 2023 Cory McIntire <cory@cpanel.net> - 1.0.3-4
- EA-11631: Build against ea-nginx version v1.25.2

* Tue Jun 20 2023 Travis Holloway <t.holloway@cpanel.net> - 1.0.3-3
- EA-11503: Build against ea-nginx version v1.25.1

* Mon May 08 2023 Dan Muey <dan@cpanel.net> - 1.0.3-2
- ZC-10395: Build/manage `modules/ngx_http_modsecurity_module.so` and nginx modsec hooks in this pkg

* Mon May 23 2022 Travis Holloway <t.holloway@cpanel.net> - 1.0.3-1
- EA-10724: Update ea-modsec30-connector-nginx from v1.0.2 to v1.0.3

* Fri Jan 14 2022 Travis Holloway <t.holloway@cpanel.net> - 1.0.2-3
- EA-10430: Add patch to support for building with nginx configured with PCRE2

* Thu Dec 16 2021 Dan Muey <dan@cpanel.net> - 1.0.2-2
- ZC-9203: Update DISABLE_BUILD to match OBS

* Mon Jun 14 2021 Cory McIntire <cory@cpanel.net> - 1.0.2-1
- EA-9863: Update ea-modsec30-connector-nginx from v1.0.1 to v1.0.2

* Wed Mar 17 2021 Tim Mullin <tim@cpanel.net> - 1.0.1-5
- EA-9421: Set SecRequestBodyLimitAction to ProcessPartial

* Mon Oct 19 2020 Daniel Muey <dan@cpanel.net> - 1.0.1-4
- ZC-7769: factor in that `active_configs` still has the vendor info even if the vendor is disabled per `active_configs`

* Thu Sep 10 2020 Daniel Muey <dan@cpanel.net> - 1.0.1-3
- ZC-7444: Remove unsupported `SecGsbLookupDb` and `SecGuardianLog` from config

* Wed Sep 02 2020 Daniel Muey <dan@cpanel.net> - 1.0.1-2
- ZC-7445: Several fixes to log directories

* Tue Aug 18 2020 Daniel Muey <dan@cpanel.net> - 1.0.1-1
- ZC-7366: initial release


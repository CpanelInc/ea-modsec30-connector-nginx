package Modsec30NginxHooks;

# cpanel - /var/cpanel/perl5/lib/Modsec30NginxHooks.pm
#                                                  Copyright 2023 cPanel, L.L.C.
#                                                           All rights Reserved.
# copyright@cpanel.net                                         http://cpanel.net
# This code is subject to the cPanel license. Unauthorized copying is prohibited

use strict;
use warnings;

use NginxHooks ();

sub describe {
    my @modsecurity_category = map {
        {
            'category' => 'ModSecurity',
            'event'    => $_,
            'stage'    => 'post',

            # NOTE: this is an admin bin, but is called on the raised
            # privileges side

            'hook'     => 'NginxHooks::_modsecurity_user',
            'exectype' => 'module',
        }
    } (
        'adjust_secruleengineoff',
    );

    my @modsec_vendor = map {
        {
            'category' => 'scripts',
            'event'    => $_,
            'stage'    => 'post',
            'hook'     => 'NginxHooks::_rebuild_global',
            'exectype' => 'module',
        }
    } (
        'modsec_vendor::add',
        'modsec_vendor::remove',
        'modsec_vendor::update',
        'modsec_vendor::enable',
        'modsec_vendor::disable',
        'modsec_vendor::enable_updates',
        'modsec_vendor::disable_updates',
        'modsec_vendor::enable_configs',
        'modsec_vendor::disable_configs',
    );

    my @global_actions = map {
        {
            'category' => 'Whostmgr',
            'event'    => $_,
            'stage'    => 'post',
            'hook'     => 'NginxHooks::_rebuild_global',
            'exectype' => 'module',
        }
    } (
        'ModSecurity::modsec_add_rule',
        'ModSecurity::modsec_add_vendor',
        'ModSecurity::modsec_assemble_config_text',
        'ModSecurity::modsec_batch_settings',
        'ModSecurity::modsec_clone_rule',
        'ModSecurity::ModsecCpanelConf::manipulate',
        'ModSecurity::modsec_deploy_all_rule_changes',
        'ModSecurity::modsec_deploy_rule_changes',
        'ModSecurity::modsec_deploy_settings_changes',
        'ModSecurity::modsec_disable_rule',
        'ModSecurity::modsec_disable_vendor',
        'ModSecurity::modsec_disable_vendor_configs',
        'ModSecurity::modsec_disable_vendor_updates',
        'ModSecurity::modsec_discard_rule_changes',
        'ModSecurity::modsec_edit_rule',
        'ModSecurity::modsec_enable_vendor',
        'ModSecurity::modsec_enable_vendor_configs',
        'ModSecurity::modsec_enable_vendor_updates',
        'ModSecurity::modsec_make_config_active',
        'ModSecurity::modsec_make_config_inactive',
        'ModSecurity::modsec_remove_rule',
        'ModSecurity::modsec_remove_setting',
        'ModSecurity::modsec_remove_vendor',
        'ModSecurity::modsec_set_config_text',
        'ModSecurity::modsec_set_setting',
        'ModSecurity::modsec_undisable_rule',
        'ModSecurity::modsec_update_vendor',
    );
    my $hook_ar = [
        @global_actions,
        @modsecurity_category,
        @modsec_vendor,
    ];

    return $hook_ar;
}

1;

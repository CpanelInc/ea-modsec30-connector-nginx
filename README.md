# mod sec 3 was alpha and is now abandoned!

## While we are determining its deprecation/EOL plan in EA4

A recent build system improvement caused two things to be aware of:

If you are one of the few using the experimental `ea-modsec30-connector-nginx` package you will need to do 2 things:

1. When you upgrade `ea-nginx` the first time to or newer you will also need to upgrade `ea-modsec30-connector-nginx` either in the same transation or afterward to keep mod sec 3 in play.
2. Anytime you change mod sec 3 rules or enable/disable mod sec 3 globally or for a user you will need to rebuild NGINX config and restart: `/usr/local/cpanel/scripts/ea-nginx confih --all`.

There is no way around item 1 and item 2 will go away in time, either when we decide to keep mod sec 3 (and add the necessary hooks to `ea-modsec30-connector-nginx`) or when we outline the deprecation plan for mod sec 3 and it goes EOL on our end.

title: Puppet and Hiera
date: 2016-05-02
description: A tutorial on Using Hiera and puppet
tags: puppet, hiera, terraform, aws, provisioningo

### What is Hiera
Hiera is a key/value lookup tool for configuration data, built to make Puppet better and let you set node-specific data without repeating yourself. 

#### Making Puppet Better
Hiera makes Puppet better by keeping site-specific data out of your manifests. Puppet classes can request whatever data they need, and your Hiera data will act like a site-wide config file.

This makes it:
* Easier to configure your own nodes: default data with multiple levels of overrides is finally easy.
* Easier to re-use public Puppet modules: don’t edit the code, just put the necessary data in Hiera.
* Easier to publish your own modules for collaboration: no need to worry about cleaning out your data before showing it around, and no more clashing variable names.

#### Avoiding Repetition
With Hiera, you can:

* Write common data for most nodes
* Override some values for machines located at a particular facility…
* …and override some of those values for one or two unique nodes.

This way, you only have to write down the differences between nodes. When each node asks for a piece of data, it will get the specific value it needs.

To decide which data sources can override which, Hiera uses a configurable hierarchy. This ordered list can include both static data sources (with names like “common”) and dynamic ones (which can switch between data sources based on the node’s name, operating system, and more).

Hiera’s config file is usually referred to as hiera.yaml. 
Use this file to configure the hierarchy, which backend(s) to use, and settings for each backend.

Hiera will fail with an error if the config file can’t be found, although an empty config file is allowed.

#### Location
By default, the config file is:

/etc/puppetlabs/code/hiera.yaml on *nix systems
COMMON_APPDATA\PuppetLabs\code\hiera.yaml on Windows

#### Changing the Config File Location
You can specify a different config file for Hiera via Puppet, the command line, or Ruby code.

##### In Puppet

You can use the hiera_config setting in puppet.conf to specify a different config file.

##### From the Command Line

You can specify a different config file with the -c (--config) option.

##### From Ruby Code

You can specify a different config file or a hash of settings when calling Hiera.new.

#### Format
Hiera’s config file must be a YAML hash. The file must be valid YAML, but may contain no data.

Each top-level key in the hash must be a Ruby symbol with a colon (:) prefix. 
The available settings are listed below, under “Global Settings” and “Backend-Specific Settings”.


##### Example Config File

	:::text
	:backends:
	  - yaml
	  - json
	:yaml:
	  :datadir: "/etc/puppetlabs/code/environments/%{::environment}/hieradata"
	:json:
	  :datadir: "/etc/puppetlabs/code/environments/%{::environment}/hieradata"
	:hierarchy:
	  - "nodes/%{::trusted.certname}"
	  - "virtual/%{::virtual}"
	  - "common"

##### Default Config Values
If the config file exists but has no data, the default settings will be equivalent to the following:

	:::text
	:backends: yaml
	:yaml:
	  # on *nix:
	  :datadir: "/etc/puppetlabs/code/environments/%{environment}/hieradata"
	  # on Windows:
	  :datadir: "C:\ProgramData\PuppetLabs\code\environments\%{environment}\hieradata"
	:hierarchy:
	  - "nodes/%{::trusted.certname}"
	  - "common"
	:logger: console
	:merge_behavior: native
	:deep_merge_options: {}

### Global Settings
The Hiera config file may contain any the following settings. If absent, they will have default values. Note that each setting must be a Ruby symbol with a colon (:) prefix.

###### :hierarchy
Must be a string or an array of strings, where each string is the name of a static or dynamic data source. (A dynamic source is simply one that contains a %{variable} interpolation token. See “Creating Hierarchies” for more details.)

The data sources in the hierarchy are checked in order, top to bottom.

Default value: ["nodes/%{::trusted.certname}", "common"]

##### :backends
Must be a string or an array of strings, where each string is the name of an available Hiera backend. The built-in backends are yaml and json. Additional backends are available as add-ons.

###### Custom backends: See “Writing Custom Backends” for details on writing new backend. Custom backends can interface with nearly any existing data store.
The list of backends is processed in order: in the example above, Hiera would check the entire hierarchy in the yaml backend before starting again with the json backend.

Default value: "yaml"

##### :logger
Must be the name of an available logger, as a string.

Loggers only control where warnings and debug messages are routed. You can use one of the built-in loggers, or write your own. The built-in loggers are:

* console (messages go directly to STDERR)
* puppet (messages go to Puppet’s logging system)
* noop (messages are silenced)
* Custom loggers: You can make your own logger by providing a class called, e.g., Hiera::Foo_logger (in which case Hiera’s internal name for the logger would be foo), and giving it class methods called warn and debug, each of which should accept a single string.

Default value: "console"; note that Puppet overrides this and sets it to "puppet", regardless of what’s in the config file.

##### :merge_behavior
Must be one of the following:

* native (default) — merge top-level keys only.
* deep — merge recursively; in the event of conflicting keys, allow lower priority values to win. You almost never want this.
* deeper — merge recursively; in the event of a conflict, allow higher priority values to win.

Anything but native requires the deep_merge Ruby gem to be installed. If you’re using Puppet Server, you’ll need to use the puppetserver gem command to install the gem.

For more details about hash merge lookup strategies, see “Hash Merge” and “Deep Merging in Hiera”.

##### :deep_merge_options
Must be a hash of options to pass to the deep merge gem, if :merge_behavior is set to deeper or deep. For example:

	:::text
	:merge_behavior: deeper
	:deep_merge_options:
	  :knockout_prefix: '--'

Available options are documented in the deep_merge gem.

##### Default value: An empty hash of options.

#### Backend-Specific Settings
Any backend can define its own settings and read them from Hiera’s config file. If present, the value of a given backend’s key must be a hash, whose keys are the settings it uses.

The following settings are available for the built-in backends:

:yaml and :json
:datadir

The directory in which to find data source files. This must be a string.

You can interpolate variables into the datadir using %{variable} interpolation tokens. This allows you to, for example, point it at "/etc/puppetlabs/code/hieradata/%{::environment}" to keep your production and development data entirely separate.

Default value: "/etc/puppetlabs/code/environments/%{environment}/hieradata" on *nix, and "C:\ProgramData\PuppetLabs\code\environments\%{environment}\hieradata" on Windows.


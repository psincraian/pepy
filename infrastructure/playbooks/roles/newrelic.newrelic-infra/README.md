[![New Relic Community Plus header](https://raw.githubusercontent.com/newrelic/open-source-office/master/examples/categories/images/Community_Plus.png)](https://opensource.newrelic.com/oss-category/#community-plus)

# Ansible role for the New Relic infrastructure agent ![test_ansible](https://github.com/newrelic/infrastructure-agent-ansible/actions/workflows/main.yml/badge.svg?branch=master) ![release_ansible](https://github.com/newrelic/infrastructure-agent-ansible/actions/workflows/release.yml/badge.svg)

An Ansible role that can be used to install and/or configure the New Relic
Infrastructure Agent and install New Relic Infrastructure OHIs.

## Installation

Use the following command to download the latest version of the New Relic role:

`ansible-galaxy install newrelic.newrelic-infra`

## Getting Started

To use the `newrelic.newrelic-infra` role directly in a playbook, simply
[include the role in your playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html#using-roles). For example,

```yaml
# myplaybook.yml
---
- hosts: webservers
  roles:
    - role: newrelic.newrelic-infra
      vars:
        nrinfragent_config:
          license_key: 12345
```

To require `newrelic.newrelic-infra` as a role depencency your own role,
[add a dependency in the meta/main.yml of your role](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html#using-role-dependencies). For example,

```yaml
# roles/myapp/meta/main.yml
---
dependencies:
  - role: newrelic.newrelic-infra
```

## Usage

This role can be used for the following interactions with the New Relic
Infrastructure Agent.

* Install the agent via OS package manager
* Install the agent via tarball (Linux only)
* Install integrations via OS package manager
* Configure the agent
* Setup the agent init service

By default, the role will install the agent via the OS package maanger,
install any integrations via the OS package manager, configure the agent, and
setup the agent init service. Additionally, the following tags are available to
perform other interactions.

* nria_install
* nria_install_tarball
* nria_install_integrations
* nria_configure
* nria_setup_service

### Basic Usage

The following snippet will install the agent via the OS package manager,
configure the agent with the specified configuration and setup the agent OS
init service.

```yaml
---
- hosts: ap_ne_1
  roles:
    - name: newrelic.newrelic-infra
      vars:
        log_file: /opt/logs/newrelic-infra.log
        verbose: 0
        nrinfragent_config:
          license_key: 12345
          custom_attributes:
            environment: dev
```

### Tarball Installation (Linux Only)

To install using the [tarball installation method](https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/linux-installation/tarball-assisted-install-infrastructure-agent-linux/
), you must set the `nrinfragent_tarball_version` variable to a valid
[tarball version number](https://download.newrelic.com/infrastructure_agent/binaries/linux/).
Installation via the tarball installation method will also run the configuration
and agent OS init service tasks unless the `nria_install_tarball` tag is
specified.

```yaml
- hosts: ap_ne_1
  roles:
    - name: newrelic.newrelic-infra
      vars:
        nrinfragent_tarball_version: 1.18.0
        nrinfragent_tarball_download_dir: /opt/newrelic/
        nrinfragent_config:
          log_file: /opt/logs/newrelic-infra.log
          verbose: 0
          license_key: 12345
          custom_attributes:
            environment: dev
```

#### Tarball installation "offline"

To use a local tarball instead of downloading it from the web you need to set
`nrinfragent_tarball_local_file_path` variable to a local path of the tarball from
`http://download.newrelic.com/infrastructure_agent/binaries/linux/{{ architecture }}/newrelic-infra_linux_{{ version }}_{{ architecture }}.tar.gz`.

```yaml
- hosts: ap_ne_1
  roles:
    - name: newrelic.newrelic-infra
      vars:
        nrinfragent_tarball_version: 1.18.0
        nrinfragent_tarball_download_dir: /opt/newrelic/
        nrinfragent_tarball_from_local: yes
        nrinfragent_config:
          log_file: /opt/logs/newrelic-infra.log
          verbose: 0
          license_key: 12345
          custom_attributes:
            environment: dev
```

### Configure Only

The following snippet will only configure the agent configuration of an existing
installation as long as the playbook is run with `--tags nria_configure`. Note
that the [`include_role`](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html#including-roles-dynamic-reuse) must be used in this case.

```yaml
- hosts: ap_ne_1
  tasks:
  - name: configure the New Relic Infrastructure Agent
    include_role:
      name: newrelic.newrelic-infra
    vars:
      nrinfragent_config:
        license_key: 12345
        log_file: /opt/logs/newrelic-infra.log
        verbose: 0
        custom_attributes:
          environment: dev
    tags:
    - nria_configure
```

## Reference

### Role configuration

#### Variables

The role configuration variables are documented [inline](defaults/main.yml)
as well as below.

##### `nrinfragent_state` (Optional)

Install or uninstall packages (package manager installation). Package manager
installations are performed using the
[Ansible package module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/package_module.html).

* `'latest'` - [default] install the latest version of the agent. Also `present`.
* `'absent'` - Uninstall the agent.

##### `nrinfragent_service_state` (Optional)

Specifies the state of the `newrelic-infra` service after install.  Defaults to
`started`, which ensures the service will be running. Change it to `stopped` to
install only, without starting it right away. See additional information about
valid values in the
[Ansible service module documentation](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html#parameter-enabled).

##### `nrinfragent_service_enabled` (Optional)

Specifies if the service will start during boot. Defauts to `yes`. change it to
`no` to prevent the service from starting automatically on boot. See additional information about
valid values in the
[Ansible service module documentation](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html#parameter-state).

##### `nrinfragent_config_file` (Optional)

Specifies a custom path on the to the New Relic Infrastructure Agent
[configuration file](https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/configuration/configure-infrastructure-agent/) on the target
hosts.  Defaults to `/etc/newrelic-infra.yml` on Linux and
`%ProgramFiles%\New Relic\newrelic-infra\newrelic-infra.yml` on Windows. This
can be especially useful on [Linux tarball installs](#tarball-installation-linux-only)
when installing to non-default locations.

##### `nrinfragent_config` (Required)

Used to populate the agent configuration. At a minimum you must provide
`license_key`. For current configuration options, see the
[New Relic documentation](https://docs.newrelic.com/docs/infrastructure/new-relic-infrastructure/configuration/configure-infrastructure-agent). For example:

```yml
custom_attributes:
  business_unit: sales
  team: newrelic
license_key: D000000000000000000000000000000000000000
log_file: /tmp/logs.log
verbose: 1
```

##### `nrinfragent_integrations` (Optional)

Specifies the On-Host Integrations to be installed via the OS package manager.
The list of available integrations can be found [here][1].

Each package should provide its `name` and `state`. The integrations package
name is located in the **Install and activate** section of the
[individual integrations docs](https://docs.newrelic.com/docs/integrations). As
a convention, their name is the name of the service with the `nri-` prefix
(`nri-apache`, `nri-redis`, etc.).

By default the state it's `absent`, which doesn't install the package; you can
change it to `latest` or `present`. For example:

```yml
nrinfragent_integrations:
  - name: nri-nginx
    state: latest
  - name: nri-mysql
    state: absent
```

The source code for each integration is available on [newrelic's GitHub organization][2].

##### license_key (DEPRECATED)

You can specify the license key via the top level `license_key` for backward
compatibility. We recommend that you use `license_key` in `nrinfragent_config`
instead. If both are specified, the one in `nrinfragent_config` takes
precedence.

##### nrinfragent_tarball_version (Required for Tarball Installation Only)

Specifies the New Relic Infrastructure agent tarball version to download.
[Linux only](https://download.newrelic.com/infrastructure_agent/binaries/linux/).

##### nrinfragent_tarball_download_dir (Required for Tarball Installation Only)

Specifies the directory on the target hosts in which to download and unzip
tarball.

##### nrinfragent_tarball_agent_dir (Optional, Tarball Installation Only)

Specifies the agent home directory path on the target hosts. Same as the
`NRIA_AGENT_DIR` [parameter] (https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/linux-installation/tarball-assisted-install-infrastructure-agent-linux/#parameters).
Defaults to `/var/db/newrelic-infra/`.

##### nrinfragent_tarball_bin_dir (Optional, Tarball Installation Only)

Specifies the agent binary directory path on the target hosts. Same as the
`NRIA_BIN_DIR` [parameter] (https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/linux-installation/tarball-assisted-install-infrastructure-agent-linux/#parameters).
Defaults to `/usr/local/bin/`.

##### nrinfragent_tarball_log_file (Optional, Tarball Installation Only)

Specifies the agent log file path on the target hosts. Same as the
`NRIA_LOG_FILE` [parameter] (https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/linux-installation/tarball-assisted-install-infrastructure-agent-linux/#parameters).
Defaults to `/var/run/newrelic-infra/newrelic-infra.log`.

##### nrinfragent_tarball_mode (Optional, Tarball Installation Only)

Specifies the agent privilege level. Same as the
`NRIA_MODE` [parameter] (https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/linux-installation/tarball-assisted-install-infrastructure-agent-linux/#parameters).
Defaults to `ROOT`.

##### nrinfragent_tarball_pid_file (Optional, Tarball Installation Only)

Specifies the agent PID file path on the target hosts. Same as the
`NRIA_PID_FILE` [parameter] (https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/linux-installation/tarball-assisted-install-infrastructure-agent-linux/#parameters).
Defaults to `/var/run/newrelic-infra/newrelic-infra.pid`.

##### nrinfragent_tarball_plugin_dir (Optional, Tarball Installation Only)

Specifies the agent plugin directory path on the target hosts. Same as the
`NRIA_PLUGIN_DIR` [parameter] (https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/linux-installation/tarball-assisted-install-infrastructure-agent-linux/#parameters).
Defaults to `/etc/newrelic-infra/integrations.d/`.

##### nrinfragent_tarball_user (Optional, Tarball Installation Only)

Specifies the user the agent binary will be run ason the target hosts. Same as
the `NRIA_USER` [parameter] (https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/linux-installation/tarball-assisted-install-infrastructure-agent-linux/#parameters).
Defaults to `root`.

##### `nrinfragent_os_name` (Optional)

Specifies the target OS that the infrastructure agent will be installed on.
Defaults to `ansible_os_family`. For a list of supported operating systems,
see the [meta/main.yml](meta/main.yml) file.

##### `nrinfragent_os_version` (Optional)

Specifies the OS version of the installer package needed for this machine.
Defaults to `ansible_lsb.major_release`. Mostly used for `RedHat` family OSs.
For a list of supported operating systems, see the
[meta/main.yml](meta/main.yml) file.

##### `nrinfragent_os_codename` (Optional)

Specifies the OS codename of the installer package needed for this machine.
Defaults to `ansible_lsb.codename`. This is used on the `Debian` family OSs.
For a list of supported operating systems, see the
[meta/main.yml](meta/main.yml) file.
****
##### `nrinfragent_choco_version` (Optional, Windows only)

Specifies the version of the Chocolatey package to install `newrelic-infra`
on Windows. Can be used to pin the version or upgrade the agent.
##### `nrinfragent_yum_lock_timeout` (Optional)

Used to set lock_timeout value for ansible yum module. When it's not set this value defaults to 30. Works only for ansible version >= 2.8.0

##### `nrinfragent_logging` (optional)

Used to generate logging file. At a minimum you must provide
`name`, `source_type`, `source_value`. For current configuration options, see the
[New Relic documentation](https://docs.newrelic.com/docs/logs/enable-log-management-new-relic/enable-log-monitoring-new-relic/forward-your-logs-using-infrastructure-agent/#parameters). To create multiple log blocks enter additional - name lists. For example:

```yml
vars:
  nrinfragent_logging:
    - name: Name of the logs that you want to forward to newrelic one [required]
      source_type: type of the logs you want to forward - file/systemd/syslog/tcp/winlog/winevtlog [required]
      source_value: ONLY FILE/SYSTEMD - value of the source type https://docs.newrelic.com/docs/logs/enable-log-management-new-relic/enable-log-monitoring-new-relic/forward-your-logs-using-infrastructure-agent/#log-source-required
      syslog: [required if source_type is syslog]
        uri: Syslog socket. Format varies depending on the protocol
        TCP/UDP network sockets - [tcp/udp]://LISTEN_ADDRESS:PORT
        Unix domain sockets unix_[tcp/udp]:// + /socket/path
        parser: Syslog parser. Default is rfc3164. Use rfc5424 if your messages include fractional seconds. Note - rfc3164 currently does not work on SuSE.
        permissions: default is 0644 for domain sockets; this limits entries to processes running as root. You can use 0666 to listen for non-root processes, at your own risk.
      tcp: [required if source_type is tcp]
        uri: TCP/IP socket to listen for incoming data. The URI format is tcp://LISTEN_ADDRESS:PORT
        format: format of the data. It can be json or none.
        separator: If format - none is used, you can define a separator string for splitting records (default - \n).
      winevtlog: [required if source_type is winevtlog]
        channel: name of the channel logs will be collected from.
        collect_eventids: a list of Windows Event IDs to be collected and forwarded to New Relic. Event ID ranges are supported.
        exclude_eventids: a list of Windows Event IDs to be excluded from collection. Event ID ranges are supported.
      winlog: [required if source_type is winlog]
        channel: name of the channel logs will be collected from.
        collect_eventids: a list of Windows Event IDs to be collected and forwarded to New Relic. Event ID ranges are supported.
        exclude_eventids: a list of Windows Event IDs to be excluded from collection. Event ID ranges are supported.
      pattern: Regular expression for filtering records. Only supported for the tail, systemd, syslog, and tcp (only with format none) sources.
      max_line_kb: Maximum size of log entries/lines in KB. If log entries exceed the limit, they are skipped. Default is 128.
      fluentbit: External Fluent Bit configuration and parser files.
        config_file: path to an existing Fluent Bit configuration file. Note that any overlapping source results in duplicate messages in New Relic Logs.
        parser_file: path to an existing Fluent Bit parsers file. The following parser names are reserved: rfc3164, rfc3164-local and rfc5424.
      custom_attributes: List of custom attributes as key-value pairs that can be used to send additional data with the logs which you can then query. Add attributes to any log source. Expects data in the following format -
      "
      custom_attributes: [
        { 'key': 'value'},
        { 'key2': 'value2'},
        ...
      ]
      "
    - name: Name of the logs that you want to forward to newrelic one [required]
      source_type: type of the logs you want to forward - file/systemd/syslog/tcp/winlog [required]
      source_value: ONLY FILE/SYSTEMD - value of the source type https://docs.newrelic.com/docs/logs/enable-log-management-new-relic/enable-log-monitoring-new-relic/forward-your-logs-using-infrastructure-agent/#log-source-required
```

#### Removing the `newrelic-infra-integrations` package and its bundled integrations

> This only applies if you have the `newrelic-infra-integrations` package
> installed

If you want to remove the `newrelic-infra-integrations` package or any of the
bundled integrations (nri-redis, nri-cassandra, nri-apache, nri-nginx,
nri-mysql), add `newrelic-infra-integrations` as the first item of
`nrinfragent_integrations` with the state `absent`.

```yml
nrinfragent_integrations:
  - name: newrelic-infra-integrations
    state: "absent"
```

## Testing

The `infrastructure-agent-ansible` role uses [molecule](https://github.com/ansible-community/molecule)
for testing. Three scenarios are provided.

1. The [default](molecule/default) scenario tests installation and
   configuration of the agent and setup of OS init services all via the OS
   package manager.
1. The [configure](molecule/configure) scenario tests running configuration
   of the agent only using the `nria_conigure` tag. Note that in order to run
   this test, the `default` scenario's `create` and `converge` method should be
   run first so the `configure` scenario has an installed agent to test with.
1. The [targz](molecule/targz) scenario tests installation and
   configuration of the agent and setup of OS init services using the tarball
   installation method.

The `default` and `targz` scenarios can be run in full using `molecule test`.
Note that the `test` command will destroy the containers after testing and
verifying the scenario.  Therefore, the best way to run the `configure` scenario
is to use `molecule converge && molecule test -s configure && molecule destroy`.

## Release to Ansible Galaxy

To release a new version to [Ansible Galaxy][3] follow this steps:

* Update the [CHANGELOG.md](CHANGELOG.md)
* Create a new GitHub release.
* Watch the build with the version number in Github Actions: https://github.com/newrelic/infrastructure-agent-ansible/actions
* Make sure the version is imported into [Ansible Galaxy][3], if there is any
  issue, ask one of the project owners.

## Compatibility

### Platforms

* RHEL/CentOS
  * RHEL/CentOS 8
  * RHEL/CentOS 7
  * RHEL/CentOS 6
  * RHEL/CentOS 5
* Ubuntu
  * 18 Bionic
  * 16 Xenial
  * 14 Trusty
  * 12 Precise
* Debian
  * 10 Buster
  * 9 Stretch
  * 8 Jessie
  * 7 Wheezy
* SUSE Linux Enterprise
  * 12
* Windows
  * All
  * _Disclaimer_: Windows support depends on the third-party
    [newrelic-infra Chocolatey package](https://chocolatey.org/packages/newrelic-infra)
    which is maintained by @ripclawffb and @xandrellas. It is distributed
    without any guarantee or support from New Relic.

## Support

New Relic hosts and moderates an online forum where customers can interact with
New Relic employees as well as other customers to get help and share best
practices. Like all official New Relic open source projects, there's a related
Community topic in the New Relic Explorers Hub. You can find this project's
topic/threads here:

* [New Relic Documentation](https://docs.newrelic.com): Comprehensive guidance for using our platform
* [New Relic Community](https://discuss.newrelic.com/c/support-products-agents/new-relic-infrastructure): The best place to engage in troubleshooting questions
* [New Relic Developer](https://developer.newrelic.com/): Resources for building a custom observability applications
* [New Relic University](https://learn.newrelic.com/): A range of online training for New Relic users of every level
* [New Relic Technical Support](https://support.newrelic.com/) 24/7/365 ticketed support. Read more about our [Technical Support Offerings](https://docs.newrelic.com/docs/licenses/license-information/general-usage-licenses/support-plan).

## Contribute

We encourage your contributions to improve [project name]! Keep in mind that
when you submit your pull request, you'll need to sign the CLA via the
click-through using CLA-Assistant. You only have to sign the CLA one time per
project.

If you have any questions, or to execute our corporate CLA (which is required
if your contribution is on behalf of a company), drop us an email at
opensource@newrelic.com.

**A note about vulnerabilities**

As noted in our [security policy](../../security/policy), New Relic is committed
to the privacy and security of our customers and their data. We believe that
providing coordinated disclosure by security researchers and engaging with the
security community are important means to achieve our security goals.

If you believe you have found a security vulnerability in this project or any of
New Relic's products or websites, we welcome and greatly appreciate you
reporting it to New Relic through [HackerOne](https://hackerone.com/newrelic).

If you would like to contribute to this project, review [these guidelines](CONTRIBUTING.md).

To all contributors, we thank you!  Without your contribution, this project
would not be what it is today.

## License

infrastructure-agent-ansible is licensed under the [Apache 2.0](http://apache.org/licenses/LICENSE-2.0.txt) License.

[1]: https://docs.newrelic.com/docs/integrations/host-integrations/host-integrations-list
[2]: https://github.com/search?l=&p=1&q=nri-+user%3Anewrelic&ref=advsearch&type=Repositories&utf8=%E2%9C%93
[3]: https://galaxy.ansible.com/newrelic/newrelic-infra

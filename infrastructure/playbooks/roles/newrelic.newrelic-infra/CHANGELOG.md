# nrinfragent Ansible role CHANGELOG

This file is used to list changes made in each version of the `nrinfragent` Ansible role.

## 0.10.4 (2021-10-28)

IMPROVEMENTS:

* Add offline support for tarball install

## 0.10.3 (2021-09-30)

IMPROVEMENTS:

* Add logging template

## 0.10.2 (2021-09-09)

IMPROVEMENTS:

* Added missing permissions to targz folders

## 0.10.1 (2021-08-31)

BUG FIXES:

* Added missing when clause for ansible version in confirm redhat lsb util is present pre2.8.0

## 0.10.0 (2021-08-26)

IMPROVEMENTS:

* Split apart `main.yml` tasks file into multiple files.
* Added tags and support for running tasks individually.
* Updated `default` molecule scenario and added `configure` and `targz`
  scenarios.
* Added additional variables for customizing tarball install.
* Added `nrinfragent_config_file` variable for customizing agent configuration
  path.
* Added support for ansible vault

BUG FIXES:

* Prevent errors on update

## 0.9.0 (2021-06-12)

BREAKING CHANGES:

* Minimal required version of ansible 2.5+

IMPROVEMENTS:

* Add support for Lock Timeout for yum (Ansible 2.8+)
* Allow user to set proxy
* Allow user to not log config values

BUG FIXES:

* Fix make cache not running on Amazon Linux
* Prevent errors on tarball install when using default values
* Ensure that log directory exists to prevent errors
* Fix installation for Windows Host

## 0.8.2 (2019-06-27)

IMPROVEMENTS:

* Add support for Windows

## 0.8.0 (2019-05-27)

IMPROVEMENTS:

* Add support for installing the agent in different linux architecture from the
  tarballs. For this purppose a new attribute was added `nrinfragent_tarball_version`.

## 0.7.0 (2019-04-08)

IMPROVEMENTS:

* Add support for installing individual integrations. The role
  switches from the deprecated `newrelic-infra-integrations` package (which
  only included 5 integrations), to the `nri-*` individual integration
  packages. The `nrinfraintegrations_state` variable was removed, a new
  `nrinfragent_integrations` variable was added for specifying individual
  integrations.

## 0.6.1 (2019-01-09)

BUG FIXES:

* Fix issue with Amazon Linux 2 install

## 0.6.0 (2018-11-23)

IMPROVEMENTS:

* Update README with better instructions for usage with Ansible Galaxy
* Installs the on-host integrations package for the Infrastructure agent
* Adds support for SUSE Linux Enterprise
* Adds support for Ubuntu Bionic
* Adds support for RHEL 5
* Fix error when specifying version number for the agent with
`nrinfragent_version`, it only worked with `nrinfragent_version: "*"` and
`nrinfragent_state: "latest"`

## 0.3.3 (2018-05-14)

BUG FIXES:

* Set default for license key

## 0.3.2 (2018-04-30)

IMPROVEMENTS:

* Replace Test Kitchen with Molecule

BUG FIXES:

* Fix Yum repository version for Amazon Linux

## 0.3.1 (2018-04-03)

BUG FIXES:

* Fix Yum repository URL for Amazon Linux

## 0.3.0 (2018-03-12)

IMPROVEMENTS:

* SUSE Linux support

## 0.2.0 (2018-01-29)

IMPROVEMENTS:

* Add `nrinfragent_config` to allow all available configuration options
* Move contents of agent.yml to main.yml

## 0.1.0 (2017-12-14)

IMPROVEMENTS:

* Initial tagged release.

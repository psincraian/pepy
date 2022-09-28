#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: merge_yaml
short_description: Merge a YAML variable with a YAML file on the host.
version_added: "1.0.0"
description: Merge a YAML variable with a YAML file on the host.
options:
    value:
        description: The dictionary to merge with src.
        required: true
        type: dict
    src:
        description: The path to a YAML file to merge 'value' into.
        required: true
        type: str
    create:
        description:
        - When true, create 'src' if it does not exist.
        - When false, fail the task if 'src' does not exist. 
        required: false
        type: bool
        default: true
    backup:
        description:
        - When true, backup 'src' if it exists by copying 'src' to a file with
        - the same name but with the current timestamp and the extension '.bak'.
        - When false, no backup of 'src' is created.
        required: false
        type: bool
        default: true
    append_lists:
        description:
        - Whether lists should be merely concatenated or "unioned".
        - By default, lists are merged by performing a "union" of each list.
        - Note that equals comparison are shallow in this case. When set to
        - 'true', lists will be blindly concatenated, the source elements being
        - appended to the target.
        required: false
        type: bool
        default: false
extends_documentation_fragment: []
author:
    - "Scott DeWitt <sdewitt@newrelic.com>"
'''

EXAMPLES = r'''
# Merge the given YAML value with a file.
# /opt/software/config.yml will be created if it does not exist.
# A backup will be created if it does exist.
- name: Merge config yaml
  merge_yaml:
    value:
        message: hello world
        nested_values:
            foo: bar
            flip: flop
        an_array:
        - one
        - two
        - shoe
    src: '/opt/software/config.yml'

# Merge the given YAML value with a file.
# Lists in 'value' will be appended to any lists in /opt/software/config.yml.
# The task will fail if /opt/software/config.yml does not exist.
# A backup will not be created if it does exist.
- name: Merge config yaml
  merge_yaml:
    value:
        message: hello world
        nested_values:
            foo: bar
            flip: flop
        an_array:
        - one
        - two
        - shoe
    src: '/opt/software/config.yml
    create: false
    backup: false
    append_lists: true
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
from datetime import datetime
import os
import shutil
import yaml

def merge_dicts(target, source, options):
    d = {}
    changed = False
    for key in target.keys():
        if not key in source:
            d[key] = target[key]
    for key in source.keys():
        if not key in target:
            d[key] = source[key]
            changed = True
            continue
        val, chg = merge(target[key], source[key], options)
        if not changed:
            changed = chg
        d[key] = val
    return (d, changed)

def merge_lists(target, source, options):
    if options['append_lists']:
        changed = len(source) > 0
        return (target + source, changed)

    changed = False
    copy = target[:]
    for item in source:
        if not item in copy:
            changed = True
            copy.append(item)
    
    return (copy, changed)


def is_mergeable(target, source):
    return (type(target) == type(source)) and \
        (isinstance(target, list) or isinstance(target, dict))

def merge(target, source, options = {}):
    if not is_mergeable(target, source):
        return (source, target != source)
    return merge_lists(target, source, options) if isinstance(target, list) \
        else merge_dicts(target, source, options)

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        value=dict(type='dict', required=True),
        src=dict(type='str', required=True),
        create=dict(type='bool', required=False, default=True),
        backup=dict(type='bool', required=False, default=True),
        append_lists=dict(type='bool', default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    the_value = module.params['value']
    the_src = module.params['src']
    append_lists = module.params['append_lists']
    should_create = module.params['create']
    should_backup = module.params['backup']
    file_exists = os.path.exists(the_src)

    if (not file_exists and not should_create) or \
       (file_exists and not os.path.isfile(the_src)):
        module.fail_json(
            msg='%s does not exist or is not a regular file' % the_src,
            **result
        )

    try:
        merged = the_value
        changed = not file_exists

        if file_exists:
            src = None
            options = {
                'append_lists': module.params['append_lists'],
            }

            with open(the_src, 'r') as f:
                src = yaml.safe_load(f.read())

            if src:
                merged, changed = merge(src, the_value, options)
                if changed and should_backup:
                    file_name = the_src + datetime.now().strftime('.%Y-%d-%m_%H%M%S.%f.bak')
                    shutil.copyfile(the_src, file_name)


        with open(module.params['src'], 'w') as f:
            f.write(yaml.dump(merged, default_flow_style=False))
    except EnvironmentError as why:
        module.fail_json(
            msg='Merge YAML failed due to OS error %s (%d)' % (why.strerror, why.errno),
            **result
        )
    except shutil.Error as why:
        module.fail_json(
            msg='Merge YAML failed due to OS error %s (%d)' % (why.strerror, why.errno),
            **result
        )


    result['changed'] = changed

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# coding: utf-8

import logging as log
import sys
import yaml

from getpass import getpass

from nornir import InitNornir
from nornir.core.plugins.connections import ConnectionPluginRegister
from nornir.core.inventory import ConnectionOptions
from nornir.core.task import Task



from os import path

from plugins.connections import Pyez
from plugins.tasks import pyez_checksum
from plugins.tasks import pyez_cmd
from plugins.tasks import pyez_commit
from plugins.tasks import pyez_config
from plugins.tasks import pyez_get_config
from plugins.tasks import pyez_diff
from plugins.tasks import pyez_rollback
from plugins.tasks import pyez_rpc
from plugins.tasks import pyez_scp

from nornir_utils.plugins.functions import print_result

FILEPATH = path.dirname(path.abspath(__file__))

NETBOX_TOKEN_FILE_DEFAULT = path.join(
    path.dirname(path.abspath(__file__)), "..", "data", "secrets.yml"
)
NETBOX_CACERT_PROD = False

def test_rpc(task: Task, target: str):
    """
    Task to check if pyez_rcp is working

    Args:
        task (Task): Nornir Task object
        target (str): Juniper XML RPC endpoint
    """
    try:
        print_result(task.run(
            task=pyez_rpc,
            func=target,
        ))
    except Exception as e:
        log.error(e)

def test_get_config(task: Task, payload: str, database: str):
    """
    Task to check if pyez_get_config is working

    Args:
        task (Task): Nornir Task object
    """
    try:
        # Can use either an XPath or a Subtree
        xml = payload
        database = database

        print_result(task.run(task=pyez_get_config, filter_xml=xml, database=database))
    except Exception as e:
        log.error(e)

def test_config(task: Task, payload: str):
    """
    Task to check if pyez_commit is working

    Args:
        task (Task): Nornir Task object
        payload (str): command line string to be executed
    """

    try: 
        config_response = task.run(
            task=pyez_config,
            payload=payload,
            data_format="set",
        )
        print_result(config_response)
        # rollback_response = task.run(pyez_rollback)
        # print_result(rollback_response)
    except Exception as e:
        log.error(e)
    
def test_diff(task: Task):
    try:
        print_result(task.run(pyez_diff))
    except Exception as e:
        log.error(e)

def test_rollback(task: Task, rollback_number: int):
    """
    Task to check if pyez_rollback is working

    Args:
        task (Task): Nornir Task object
        rollback_number (int): number of the rollback configuration to restore
    """
    try:
        print_result(task.run(
            task=pyez_rollback,
            rollback_number=rollback_number,
        ))
    except Exception as e:
        log.error(e)

def test_commit(task: Task):
    """
    Task to check if pyez_commit is working

    Args:
        task (Task): Nornir Task object
    """
    try:
        print_result(task.run(
            task=pyez_commit,
        ))
    except Exception as e:
        log.error(e)

def test_scp(task: Task, file: str, path: str):
    """
    Task to check to copy file with SCP

    Args:
        task (Task): Nornir Task object
        file (str): filename of the file to be copied
        path (str): remote path where to put the file
        dryrun (bool): if true set dryrun
    """
    try:
        scp_response = task.run(
            task=pyez_scp,
            file=f"{FILEPATH}/{file}",
            path=path,
        )
        print_result(scp_response)
    except Exception as e:
        log.error(e)

def test_checksum(task: Task, file: str, path: str):
    """
    Task to check if pyez_checksum is working

    Args:
        task (Task): Nornir Task object
    """
    try:
        print_result(task.run(
            task=pyez_checksum,
            filepath=f"{path}/{file}",
            calc="sha256"
        ))
    except Exception as e:
        log.error(e)

def test_cmd(task: Task, command: str):
    """
    Task to check to pyez_cmd

    Args:
        task (Task): Nornir Task object
        command (str): shell command to execute 
    """
    try:
        scp_response = task.run(
            task=pyez_cmd,
            command=command
        )
        print_result(scp_response)
    except Exception as e:
        log.error(e)


    
def netbox_inventory(
    token_file=NETBOX_TOKEN_FILE_DEFAULT,
    token_name="pancom_ro",
    netbox_url="https://netbox.plabs.ch",
    verify=NETBOX_CACERT_PROD,
    filters={"name": "T-CHSH1-LF02-SEC"},
    debug=False,
    logging=False,
):

    # To be replaced by Vault when available
    try:
        with open(token_file, "r") as fd:
            config = yaml.load(fd, Loader=yaml.SafeLoader)
            token = config["netbox"]["token"][token_name]
    except Exception as e:  # FIXME: exception is not correctly handled
        log.error(
            "__init__: error while loading config from {}: {}".format(
                token_file, e
            )
        )
        raise e

    nr = InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 100,
            },
        },
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": netbox_url,
                "nb_token": token,
                "filter_parameters": filters,
                "ssl_verify": verify,
            },
        },
        logging={"enabled": logging},
    )

    nr.inventory.defaults.port = 22

    # nr.run(task=test_rpc)
    return nr

def main():
    password = getpass()

    ConnectionPluginRegister.register("pyez", Pyez)

    nr = netbox_inventory()

    nr.inventory.defaults.username = "gegger"
    nr.inventory.defaults.password = password

    # Trick to use ssh key
    extras = {}
    # if privkey:
    extras["ssh_private_key_file"] = "/home/gegger/.ssh/id_network"

    nr.inventory.defaults.connection_options["pyez"] = ConnectionOptions(
        extras=extras
    )

    # nr.run(task=test_rpc, target="get-firmware-information")
    # nr.run(task=test_get_config, payload="<configuration><interfaces/><vlans/></configuration>", database="committed")
    
    # # First try to config  (but not commit) and rollback + unlock
    # nr.run(task=test_config, payload="set system host-name BOU")
    # nr.run(task=test_diff)
    # nr.run(task=test_rollback, rollback_number=0)
    # # Then try to commit changes
    # nr.run(task=test_config, payload="set system host-name BOU")
    # nr.run(task=test_diff)
    # nr.run(task=test_commit)
    # # Eventually try to rollback to previous conf and commit
    # nr.run(task=test_rollback, rollback_number=1)
    # nr.run(task=test_commit)
    nr.run(task=test_scp, file="test.txt", path="/var/tmp/")
    nr.run(task=test_checksum, file="test.txt", path="/var/tmp/")
    nr.run(task=test_cmd, command="uptime")


if __name__ == "__main__":
    main()
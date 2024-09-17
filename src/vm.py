## python script to list all gce vms   
import sys
import os
import re
import json
from google.cloud import compute_v1

def list_vms(project_id):
    """
    List all Compute Engine instances in a project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.

    Returns:
        A list of Compute Engine instances.
    """
    instance_client = compute_v1.InstancesClient()
    instances = instance_client.list(project=project_id)

    return instances

def main():
    """
    Entry point for the script.
    """
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <project_id>")
        sys.exit(1)

    project_id = sys.argv[1]
    instances = list_vms(project_id)

    for instance in instances:
        print(f" - {instance.name} ({instance.machine_type})")

if __name__ == "__main__":
    main()
# Generate python function to list all google cloud virtual machines within a project
def list_vms():
    """Lists all VMs."""
    compute_client = compute.Client()

    # Note: Client.list_instances requires at least package version 1.17.0.
    instances = list(compute_client.list_instances())

    print("Instances:")
    for instance in instances:
        print(instance.name)

    return instances
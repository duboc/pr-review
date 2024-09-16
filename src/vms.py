import google.cloud.compute_v1 as compute_v1


def list_instances(project_id, zone):
    """
    Lists all instances in the given project and zone.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
    """
    instance_client = compute_v1.InstancesClient()

    # List of all instances in the specified project and zone.
    request = compute_v1.ListInstancesRequest()
    request.project = project_id
    request.zone = zone

    instances = instance_client.list(request=request)

    if not instances:
        print("No instances found in project {} and zone {}".format(project_id, zone))
        return

    print("Instances in project {} and zone {}:".format(project_id, zone))
    for instance in instances:
        print("- {}".format(instance.name))


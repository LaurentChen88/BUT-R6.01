from pulumi_gcp import cloudrunv2


default = cloudrunv2.Service(
    'default',
    name='cloudrun-service',
    location='europe-west9',
    deletion_protection=False,
    ingress="INGRESS_TRAFFIC_ALL",
    template={
        "containers": [{
            "image": "us-docker.pkg.dev/cloudrun/container/hello",
        }],
    })

from pulumi_gcp import projects

from tp3.config import PROJECT, STUDENTS_GROUP


projects.IAMBinding(
    'list-buckets-binding',
    project=PROJECT,
    role="roles/storage.objectViewer",
    members=['group:' + STUDENTS_GROUP],
)

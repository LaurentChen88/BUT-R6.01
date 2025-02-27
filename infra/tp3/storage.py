import glob
import os
import re

import pulumi
from pulumi_gcp import storage

from tp3.config import STUDENTS_GROUP, STUDENT_ACCOUNTS, SOURCE_DATA_DIR


bucket = storage.Bucket(
    'but-tp-shazam-datalake',
    name='but-tp-shazam-datalake',
    location='europe-west9'
)


storage.BucketIAMBinding(
    'shazam-datalake-binding',
    bucket=bucket.name,
    role="roles/storage.objectViewer",
    members=['group:' + STUDENTS_GROUP],
)


storage.BucketObject(
    'metadata.csv',
    name='metadata.csv',
    bucket=bucket.name,
    source=pulumi.FileAsset(os.path.join(SOURCE_DATA_DIR, 'metadata.csv'))
)


for vector_file_name in glob.glob(os.path.join(SOURCE_DATA_DIR, 'vectors_*.jsonl')):
    object_name = os.path.join('tracks', os.path.basename(vector_file_name))
    storage.BucketObject(
        object_name,
        name=object_name,
        bucket=bucket.name,
        source=pulumi.FileAsset(vector_file_name)
    )


storage.BucketObject(
    'queries.jsonl',
    name='queries/queries.jsonl',
    bucket=bucket.name,
    source=pulumi.FileAsset(os.path.join(SOURCE_DATA_DIR, 'queries.jsonl'))
)

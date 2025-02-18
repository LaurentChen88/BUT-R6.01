import glob
import os

import pulumi
from pulumi_gcp import storage

from tp3.config import STUDENTS_GROUP


bucket = storage.Bucket(
    'but-tp-shazam-data',
    name='but-tp-shazam-data',
    location='europe-west9'
)


storage.BucketObject(
    'metadata.csv',
    name='metadata.csv',
    bucket=bucket.name,
    source=pulumi.FileAsset('tp3/data/metadata.csv')
)


for vector_file_name in glob.glob('tp3/data/*.jsonl'):
    object_name = os.path.join('songs', os.path.basename(vector_file_name))
    storage.BucketObject(
        object_name,
        name=object_name,
        bucket=bucket.name,
        source=pulumi.FileAsset(vector_file_name)
    )


storage.BucketIAMBinding(
    'shazam-data-binding',
    bucket=bucket.name,
    role="roles/storage.objectViewer",
    members=['group:' + STUDENTS_GROUP],
)


pulumi.export('shazam_data_url', bucket.url)

import glob
import os
import re

from pulumi_gcp import storage, compute

from tp3.config import STUDENT_ACCOUNTS


gce_account = compute.get_default_service_account()

for account in STUDENT_ACCOUNTS:
    account_bucket_name = 'but-tp-shazam' + re.sub(r'@.*', '', account)
    account_bucket = storage.Bucket(
        account_bucket_name,
        name=account_bucket_name,
        location='europe-west9'
    )
    storage.BucketIAMBinding(
        f'shazam-{account_bucket_name}-binding',
        bucket=account_bucket.name,
        role="roles/storage.objectUser",
        members=[
            'user:' + account,
            'serviceAccount:' + gce_account.email
        ],
    )

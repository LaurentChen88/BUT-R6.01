import re

from pulumi_gcp import bigquery

from tp3.config import STUDENTS_GROUP, ADMIN_ACCOUNT, STUDENT_ACCOUNTS


shared_dataset = bigquery.Dataset(
    'shared-dataset',
    dataset_id='shared',
    location='europe-west9',
    accesses=[
        {'role': 'READER', 'group_by_email': STUDENTS_GROUP}
    ]
)


for account in STUDENT_ACCOUNTS:
    dataset_name = re.sub(r'@.*', '', account)
    bigquery.Dataset(
        dataset_name + '-dataset',
        dataset_id=dataset_name,
        location='europe-west9',
        accesses=[
            {'role': 'OWNER', 'user_by_email': account},
            {'role': 'OWNER', 'user_by_email': ADMIN_ACCOUNT},
        ]
    )

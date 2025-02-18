import json
import re

from pulumi_gcp import bigquery

from tp3.config import PROJECT, STUDENTS_GROUP, ADMIN_ACCOUNT, STUDENT_ACCOUNTS


shared_dataset = bigquery.Dataset(
    'shared-dataset',
    dataset_id='shared',
    location='europe-west9',
    accesses=[
        {'role': 'READER', 'group_by_email': STUDENTS_GROUP}
    ]
)


JOIN_VECTORS_BODY = f'''
    SELECT x, vec2[SAFE_OFFSET(position)] AS y
    FROM UNNEST(vec1) AS x WITH OFFSET AS position
'''

FLOAT64_ARRAY_TYPE = json.dumps({
    'typeKind': 'ARRAY',
    'arrayElementType': {
        'typeKind': 'FLOAT64'
    }
})

bigquery.Routine(
    'join_vectors',
    dataset_id=shared_dataset.dataset_id,
    routine_id='join_vectors',
    routine_type='TABLE_VALUED_FUNCTION',
    language='SQL',
    definition_body=JOIN_VECTORS_BODY,
    arguments=[
        {
            'name': 'vec1',
            'argument_kind': 'FIXED_TYPE',
            'data_type': FLOAT64_ARRAY_TYPE
        },
        {
            'name': 'vec2',
            'argument_kind': 'FIXED_TYPE',
            'data_type': FLOAT64_ARRAY_TYPE
        }
    ],
    return_table_type=json.dumps({
        'columns': [
            {
                'name': 'x',
                'type': {'typeKind': 'FLOAT64'}
            },
            {
                'name': 'y',
                'type': {'typeKind': 'FLOAT64'}
            }
        ]
    })
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

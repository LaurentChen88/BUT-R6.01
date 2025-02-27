import io
import os

import librosa
import numpy as np
import tensorflow as tf
import functions_framework
from google.cloud import storage
import minihub


storage_client = storage.Client()
model = minihub.get_yamnet_model()


@functions_framework.http
def process_file(request):
    request_json = request.get_json(silent=True)

    bucket_name = request_json['bucket']
    object_name = request_json['name']

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    with blob.open('rb') as f:
        input_frames, _ = librosa.load(f, sr=16_000, mono=True, dtype=np.float32)
    _, embeddings, _ = model(input_frames)

    return {
        'base_name': os.path.basename(object_name),
        'embeddings': embeddings
    }

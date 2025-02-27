
import os
import io
import requests
import tensorflow as tf
import tarfile


MODEL_DIR = '/tmp/minihub'


def extract_file(tgz,
                 tarinfo,
                 dst_path,
                 buffer_size=10 << 20):
  """Extracts 'tarinfo' from 'tgz' and writes to 'dst_path'."""
  src = tgz.extractfile(tarinfo)
  if src is None:
    return
  dst = tf.compat.v1.gfile.GFile(dst_path, "wb")
  while 1:
    buf = src.read(buffer_size)
    if not buf:
      break
    dst.write(buf)
  dst.close()
  src.close()


def extract_tarfile_to_destination(fileobj, dst_path):
  """Extract a tarfile. Optional: log the progress."""
  with tarfile.open(mode="r|*", fileobj=fileobj) as tgz:
    for tarinfo in tgz:
      abs_target_path = merge_relative_path(dst_path, tarinfo.name)

      if tarinfo.isfile():
        extract_file(tgz, tarinfo, abs_target_path)
      elif tarinfo.isdir():
        tf.compat.v1.gfile.MakeDirs(abs_target_path)
      else:
        # We do not support symlinks and other uncommon objects.
        raise ValueError("Unexpected object type in tar archive: %s" %
                         tarinfo.type)


def merge_relative_path(dst_path, rel_path):
  """Merge a relative tar file to a destination (which can be "gs://...")."""
  # Convert rel_path to be relative and normalize it to remove ".", "..", "//",
  # which are valid directories in fileystems like "gs://".
  norm_rel_path = os.path.normpath(rel_path.lstrip("/"))

  if norm_rel_path == ".":
    return dst_path

  # Check that the norm rel path does not starts with "..".
  if norm_rel_path.startswith(".."):
    raise ValueError("Relative path %r is invalid." % rel_path)

  merged = os.path.join(dst_path, norm_rel_path)

  # After merging verify that the merged path keeps the original dst_path.
  if not merged.startswith(dst_path):
    raise ValueError("Relative path %r is invalid. Failed to merge with %r." %
                     (rel_path, dst_path))
  return merged


def get_yamnet_model():
    url = 'https://tfhub.dev/google/yamnet/1?tf-hub-format=compressed'
    r = requests.get(url)
    data = io.BytesIO(r.content)
    extract_tarfile_to_destination(data, MODEL_DIR)
    return tf.compat.v1.saved_model.load_v2(MODEL_DIR)

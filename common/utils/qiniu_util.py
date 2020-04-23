import os
import sys

from qiniu import Auth

QINIU_SECRET_KEY = os.environ.get("QINIU_SECRET_KEY")
QINIU_ACCESS_KEY = os.environ.get("QINIU_ACCESS_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")


def get_upload_token() -> str:
    try:
        q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
        token = q.upload_token(BUCKET_NAME)
        return token
    except Exception as e:
        sys.stderr.write(e)
        return ""

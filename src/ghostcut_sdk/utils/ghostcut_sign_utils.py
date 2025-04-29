# -*- coding: utf-8 -*-

import hashlib

def generate_ghostcut_sign(body: str, appSecret: str):
    md5_1 = hashlib.md5()
    md5_1.update(body.encode('utf-8'))
    body_md5hex = md5_1.hexdigest()
    md5_2 = hashlib.md5()
    body_md5hex = (body_md5hex + appSecret).encode('utf-8')
    md5_2.update(body_md5hex)

    sign = md5_2.hexdigest()

    return sign
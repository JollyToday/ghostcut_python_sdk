import hashlib
import json
import uuid

def generate_nonce() -> str:
    """生成随机的 nonce 字符串"""
    return str(uuid.uuid4())

def calculate_md5(data: str) -> str:
    """计算字符串的 MD5 值"""
    md5_hash = hashlib.md5()
    md5_hash.update(data.encode('utf-8'))
    return md5_hash.hexdigest()

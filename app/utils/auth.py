import os
import re
import hmac
import base64
import time
import json
import hashlib
from urllib.parse import urlencode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


def valid_password(password):
    """
        验证密码是否符合以下要求：
        1. 长度在6到32位之间
        2. 只包含字母（大小写）、数字和以下特殊字符：!@#$%^&*()_-+=[]{}|;:',.<>?/

    :param password: 明文密码
    :return:
    """
    password_length = len(password)
    allowed_chars_pattern = r'^[A-Za-z0-9!@#$%^&*()_\-=+\\[\]{}|;:\'",.<>?/]*$'
    if 6 <= password_length <= 32 and re.match(allowed_chars_pattern, password):
        return True
    else:
        return False


def encrypt_request_sign(hmac_key: bytes, public_key, api: str, body: dict, params: dict):
    timestamp = int(time.time())
    nonce = base64.b64encode(os.urandom(16)).decode('utf-8')
    data = f'{timestamp},{nonce}'
    body_encoded = urlencode(body, doseq=True)
    params_encoded = urlencode(params, doseq=True)
    sign_data = f'{data},{api},{body_encoded},{params_encoded}'
    encrypted_data = public_key.encrypt(
        data.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    x_sign = hmac.new(hmac_key, sign_data.encode('utf-8'), hashlib.sha256).hexdigest()
    x_data = base64.b64encode(encrypted_data).decode('utf-8')
    return x_sign, x_data


def parse_response_data(public_key, combined_data):
    try:
        decoded_data = base64.b64decode(combined_data)
        data, signature = decoded_data.split(b'::', 1)
        public_key.verify(
            signature,
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        result = json.loads(data)
        timestamp = result['time']
        if abs(time.time() - timestamp) > 50:
            raise TimeoutError
        return data
    except (InvalidSignature, KeyError, TimeoutError):
        return None

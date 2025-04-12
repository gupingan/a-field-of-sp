import hashlib
import subprocess
import wmi
import string
import uuid
import re

from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L


def validate(pc_id: str):
    """
    校验机器码
    :param pc_id: PC ID
    :return:
    """
    pattern = r'^[0-9a-f]{64}$'
    return bool(re.match(pattern, pc_id))


def get_pc_id(gpa_timestamp: str) -> str:
    try:
        bios = wmi.WMI().Win32_BIOS()[0]
        bios_id = bios.SerialNumber.strip()
    except (IndexError, AttributeError):
        bios_id = 'khs-uuid'

    try:
        os_id = subprocess.check_output('wmic csproduct get UUID', shell=True).decode().split('\n')[1].strip()
    except subprocess.CalledProcessError:
        os_id = 'khs-uuid'

    combined_string = f"{gpa_timestamp}_{bios_id}_{os_id}"
    hash_object = hashlib.sha256(combined_string.encode())
    software_id = hash_object.hexdigest()

    return software_id


def generate_qr_code(pc_id):
    qr = QRCode(
        version=1,
        box_size=5,
        border=2,
        error_correction=ERROR_CORRECT_L
    )
    qr.add_data(pc_id)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="transparent")


def get_short_id():
    """
    获取短 ID
    :return: str 8位 短ID
    """
    _array = string.digits + string.ascii_letters
    _id = str(uuid.uuid4()).replace('-', '')
    buffer = []
    for i in range(0, 8):
        start = i * 4
        end = (i + 1) * 4
        val = int(_id[start: end], 16)
        buffer.append(_array[val % 62])

    return ''.join(buffer)

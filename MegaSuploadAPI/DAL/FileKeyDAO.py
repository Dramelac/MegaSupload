import base64
import binascii
import os

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from django.core.exceptions import ObjectDoesNotExist

from MegaSuploadAPI.models import FileKey


def newFileKey(owner, file, uncrypted_key=binascii.hexlify(os.urandom(20))):
    # genereration password (20)=> chiffrement rsa de celui si avec user pub_key
    # Will raise NotImplementedError if random is not available on the system

    pub_key = RSA.import_key(owner.pub_key.encode('utf8'))
    cipher_rsa = PKCS1_OAEP.new(pub_key)
    key = base64.b64encode(cipher_rsa.encrypt(uncrypted_key))

    FileKey.objects.create(owner=owner, file=file, key=key.decode("utf8"))
    return uncrypted_key


def remove(owner, file):
    key = FileKey.objects.get(file=file, owner=owner)
    if key is not None:
        key.delete()


def getFileKey(owner, file):
    fileKey = FileKey.objects.get(file=file, owner=owner)
    if fileKey is not None:
        return fileKey
    else:
        raise ObjectDoesNotExist
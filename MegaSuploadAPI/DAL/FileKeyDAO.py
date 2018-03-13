import binascii
import base64
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from django.core.exceptions import ObjectDoesNotExist

from MegaSuploadAPI.models import FileKey


def newFileKey(owner, file):
    # genereration password (20)=> chiffrement rsa de celui si avec user pub_key
    # Will raise NotImplementedError if random is not available on the system

    uncrypted_key = binascii.hexlify(os.urandom(20))
    pub_key = RSA.import_key(owner.pub_key)
    cipher_rsa = PKCS1_OAEP.new(pub_key)
    key = base64.b64encode(cipher_rsa.encrypt(uncrypted_key))

    FileKey.objects.create(owner=owner, file=file, key=key)


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

import base64
import bcrypt
import hashlib

class HashService:
    """
    Service encapsulating password-related functionality e.g. hashing and verification.
    """

    @classmethod
    def hash(cls, plain_text):
        """
        Given a plain text password, return it's bcrypt hash.
        The password is first hashed via SHA-256 then B64-encoded to prevent
        null byte issues and circumvent the 72-char limit imposed by bcrypt.
        """
        sha256_encoded = hashlib.sha256(plain_text.encode('utf-8'))
        b64_encoded = base64.b64encode(sha256_encoded.digest())

        return bcrypt.hashpw(b64_encoded, bcrypt.gensalt()).decode('utf-8')

    @classmethod
    def verify(cls, plain_text, hashed):
        """
        Given a plain_text password and a bcrypt hash, check if it matches the hash.
        The plain test password is pre-hashed identically to the hash() function.
        """
        sha256_encoded = hashlib.sha256(plain_text.encode('utf-8'))
        b64_encoded = base64.b64encode(sha256_encoded.digest())

        return bcrypt.checkpw(b64_encoded, hashed.encode('utf-8'))

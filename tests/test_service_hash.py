
from src.services.hash import HashService

class TestHashService:

    def test_verify_success(self):
        plain_text = 'my password'
        hashed = '$2b$12$ez1dc6f8iVqjzBFijp4bCOpCOvePkzXsPLbHMfbtDz3CspX9SjPKO'

        assert HashService.verify(plain_text, hashed) == True

    def test_verify_fail(self):
        plain_text = 'wrong password'
        hashed = '$2b$12$ez1dc6f8iVqjzBFijp4bCOpCOvePkzXsPLbHMfbtDz3CspX9SjPKO'

        assert HashService.verify(plain_text, hashed) == False

    def test_verify_raw_success(self):
        raw_data = bytearray(b'\xde\xf3\xa5Y\n\x03\xae:c\x9c')
        hashed = b'$2b$12$ePKDJSGf7ukZMq4HOx.f/.WBL5obXuHcZY4fR6u3Hf1C6cqqCyc8u'

        assert HashService.verify_raw(raw_data, hashed) is True

    def test_verify_raw_fail(self, private_key_n_bytes):
        raw_data = private_key_n_bytes(12)
        hashed = b'$2b$12$ePKDJSGf7ukZMq4HOx.f/.WBL5obXuHcZY4fR6u3Hf1C6cqqCyc8u'

        assert HashService.verify_raw(raw_data, hashed) is False

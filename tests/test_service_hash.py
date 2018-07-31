
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

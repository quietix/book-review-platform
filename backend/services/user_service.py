import bcrypt


class UserService:
    @staticmethod
    def get_hashed_password(password: str):
        try:
            byte_pass = password.encode('utf-8')
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(byte_pass, salt)
        except UnicodeEncodeError:
            raise ValueError("Password contains unsupported characters.")
        except ValueError:
            raise ValueError("Error while hashing the password.")
        except Exception as e:
            raise RuntimeError("An unexpected error occurred.") from e

    @staticmethod
    def verify_password(password_to_verify: str, original_pass: bytes) -> bool:
        try:
            byte_pass = password_to_verify.encode('utf-8')
            return bcrypt.checkpw(byte_pass, original_pass)
        except UnicodeEncodeError:
            raise ValueError("Password contains unsupported characters.")
        except ValueError:
            raise ValueError("Error during password verification.")
        except Exception as e:
            raise RuntimeError("An unexpected error occurred during password verification.") from e

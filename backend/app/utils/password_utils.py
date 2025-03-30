import bcrypt


def hash_password(password):
    """
    Hash a password for storing.

    Args:
        password (str): The password to hash

    Returns:
        str: The hashed password
    """
    # Generate a salt and hash the password
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Return the hashed password as a string
    return hashed.decode("utf-8")


def check_password(password, hashed_password):
    """
    Verify a stored password against a provided password.

    Args:
        password (str): The password to check
        hashed_password (str): The stored hashed password

    Returns:
        bool: True if the password matches, False otherwise
    """
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    # Check that the provided password matches the stored password
    return bcrypt.checkpw(password_bytes, hashed_bytes)

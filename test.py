from cryptography.fernet import Fernet
key = Fernet.generate_key()

secret_key = b'BrzB6MUAmWWzMUS6gA03Lwei8SKaTRIQGfXvvKVUsZE='

f = Fernet(secret_key)

message = "my deep dark secret"
encoded_message = message.encode()

encrypted = f.encrypt(encoded_message)

print(encrypted.decode())

decrypted = f.decrypt(encrypted)
print(decrypted)
print(decrypted.decode())
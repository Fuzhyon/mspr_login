import pyotp

# generating TOTP codes with provided secret
print(pyotp.random_hex())
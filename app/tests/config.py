from passlib.context import CryptContext

pwd = CryptContext(schemes=['bcrypt'])
print(pwd.hash('1'))
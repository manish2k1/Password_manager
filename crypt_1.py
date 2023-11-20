import hashlib

import cryptography
import backend
import base64
from cryptography.fernet import Fernet

# GLOBAL PASSWORD
masterpassword=''
new_masterpassword=''


# DECRYPTION WITH MASTERPASSWORD AND VARIABLE
def test_masterpassword(master_password, cypher_text):          
    
    md5_hash = hashlib.md5()

    md5_hash.update(master_password.encode())

    md5_hash_hex = md5_hash.hexdigest()

    byte_stream1 = md5_hash_hex.encode('utf-8') 

    base64_urlsafe = base64.urlsafe_b64encode(byte_stream1).decode()

    key=base64_urlsafe
    cipher_suite = Fernet(key)

    decrypted_text_bs=cipher_suite.decrypt(cypher_text.encode('utf-8'))

    decrypted_text = decrypted_text_bs.decode('utf-8')
    return(decrypted_text)

# ENCRYPTION WITH MASTERPASSWORD AND VARIABLE
def write_encrypt_password(master_password, simple_text):

    md5_hash = hashlib.md5()

    md5_hash.update(master_password.encode())

    md5_hash_hex = md5_hash.hexdigest()

    byte_stream1 = md5_hash_hex.encode('utf-8') 

    base64_urlsafe = base64.urlsafe_b64encode(byte_stream1).decode()

    key=base64_urlsafe
    cipher_suite = Fernet(key)

    encrypted_text_bs=cipher_suite.encrypt(simple_text.encode('utf-8'))

    encrypted_text = encrypted_text_bs.decode('utf-8')
    return(encrypted_text)

# ENCRYPTION WITH VARIABLE
def encrypt_text(simple_text):

    md5_hash = hashlib.md5()

    md5_hash.update(masterpassword.encode())

    md5_hash_hex = md5_hash.hexdigest()

    byte_stream1 = md5_hash_hex.encode('utf-8') 

    base64_urlsafe = base64.urlsafe_b64encode(byte_stream1).decode()

    key=base64_urlsafe
    cipher_suite = Fernet(key)

    encrypted_text_bs=cipher_suite.encrypt(simple_text.encode('utf-8'))

    encrypted_text = encrypted_text_bs.decode('utf-8')
    return(encrypted_text)


# DECRYPTION WITH VARIABLE
def decrypt_text(cypher_text):

    md5_hash = hashlib.md5()

    md5_hash.update(masterpassword.encode())

    md5_hash_hex = md5_hash.hexdigest()

    byte_stream1 = md5_hash_hex.encode('utf-8') 

    base64_urlsafe = base64.urlsafe_b64encode(byte_stream1).decode()

    key=base64_urlsafe
    cipher_suite = Fernet(key)

    decrypted_text_bs=cipher_suite.decrypt(cypher_text.encode('utf-8'))

    decrypted_text = decrypted_text_bs.decode('utf-8')
    return(decrypted_text)

# TEST MASTERPASS FUNCTION
def logon(password):
    
    data = backend.retrieve_user()
    for value in data:
        
        phrase = value[2]
        
        try:
            decrypted_password = test_masterpassword(phrase, value[1])

            
            if decrypted_password == password:
                global masterpassword
                masterpassword = password
                return 1  
            else:
                return 0
        except cryptography.fernet.InvalidToken:
            return 3 

# REPLACE PAST DATA WITH NEW DATA        
def new_encrypt_text(simple_text):

    md5_hash = hashlib.md5()

    md5_hash.update(new_masterpassword.encode())

    md5_hash_hex = md5_hash.hexdigest()

    byte_stream1 = md5_hash_hex.encode('utf-8') 

    base64_urlsafe = base64.urlsafe_b64encode(byte_stream1).decode()

    key=base64_urlsafe
    cipher_suite = Fernet(key)

    encrypted_text_bs=cipher_suite.encrypt(simple_text.encode('utf-8'))

    encrypted_text = encrypted_text_bs.decode('utf-8')
    return(encrypted_text)

def replace_data(data):
    
    decrypted_data = decrypt_text(data)
    new_encrypted_data = new_encrypt_text(decrypted_data)
    return new_encrypted_data


# ENCRYPT PRESENT DATA WITH NEW MASTERPASS
def replace(npw):
    
    global new_masterpassword
    new_masterpassword = npw
    
    record = backend.retrieve()
    
    for value in record:
        sl_no = value[0]
        new_title = replace_data(value[1])
        new_username = replace_data(value[2])
        new_password = replace_data(value[3])
        new_notes = replace_data(value[4])
        new_LM = replace_data(value[5])
        
        backend.update_record(sl_no, new_title, new_username, new_password, new_notes, new_LM)
    global masterpassword
    masterpassword = new_masterpassword
    return
        
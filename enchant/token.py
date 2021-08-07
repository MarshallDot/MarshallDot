import keyring

service_id = 'SHELL'
token = input("Token: ")
keyring.set_password(service_id, service_id, token)

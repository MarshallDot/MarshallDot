from keyring import set_password
import getpass

service_id = 'SHELL'
token = getpass.getpass(prompt='Token: ', stream=None)
set_password(service_id, service_id, token)

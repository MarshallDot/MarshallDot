from keyring import set_password
import getpass

service_id = 'VALVEDB'
token = getpass.getpass(prompt='Password: ', stream=None)
set_password(service_id, service_id, token)

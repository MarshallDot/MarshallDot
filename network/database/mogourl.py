from keyring import set_password
import getpass

service_id = 'MogoMar'
url = input('Mongo DB url: ')
set_password(service_id, service_id, url)
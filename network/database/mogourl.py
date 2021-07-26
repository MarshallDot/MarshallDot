from keyring import set_password
import getpass

service_id = 'MogoMar'
url = getpass.getpass(prompt='Mongo DB url: ', stream=None)
set_password(service_id, service_id, url)
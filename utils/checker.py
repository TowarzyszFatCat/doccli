from apis import docchi, aniskip
from termcolor import colored

def service_statuses():
    docchi_status = docchi.check_service_availability()
    aniskip_status = aniskip.check_service_availability()
    return f"Docchi: {docchi_status} | Aniskip: {aniskip_status}"




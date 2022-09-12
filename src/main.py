import logging

from service import CiscoService
from config.settings import dev_settings, srv_settings

_log_format = ("%(asctime)s - [%(levelname)s] - %(name)s "
               "(%(filename)s).%(funcName)s(%(lineno)d) > %(message)s")
logging.basicConfig(filename='./output/logs.log',
                    level=logging.INFO,
                    format=_log_format,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

logger.info('Start of data collection from the switch')

cisco = CiscoService(settings=dev_settings.dict())

ver = cisco.get_version()
start_conf = cisco.get_startup_config()
run_conf = cisco.get_running_config()
acl = cisco.get_acl()
interfaces = cisco.get_interfaces()

cisco.close()

logger.info('Data collection completed successfully')

with open('./output/results.txt', 'w') as file:
    file.write(f'Hostname: {ver.get("hostname")}\n')
    file.write(f'Version: {ver.get("version")}\n')
    file.write(2 * '\n')
    file.write(f'Starting configuration file: {srv_settings.start_cfg_file}\n')
    file.write(f'Current configuration file: {srv_settings.run_cfg_file}\n')
    file.write(2 * '\n')
    file.write('Information about Switch Access Control Lists (ACLs):\n')
    file.write(acl.get_string() + '\n')
    file.write(2 * '\n')
    file.write('Information about Switch interfaces:\n')
    file.write(interfaces.get_string())

from pytpp import Authenticate, Features, logger
import logging


logging.basicConfig(level=logging.DEBUG)
l = logging.getLogger('pytpp')

logger.msg_char_limit = 10
api = Authenticate('10.100.208.84', 'admin', 'newPassw0rd!')
features = Features(api)

features.objects.get(r'\VED\Policy')
features.platforms.ssh_certificate_manager.update_engines()

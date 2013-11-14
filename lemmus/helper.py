
import inspect
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def importLib(library):
	try:
		logger.debug('Importing %s',library)
		return __import__(library)
	except:
		logger.error('Failed to import [%s]',library) 
		exit(1)		
	


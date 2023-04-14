import logging

# configurar el registro
logging.basicConfig(filename='example.log', level=logging.DEBUG)

# ejemplo de registro
logging.debug('Este es un mensaje de depuración')
logging.info('Este es un mensaje de información')
logging.warning('Este es un mensaje de advertencia')
logging.error('Este es un mensaje de error')
logging.critical('Este es un mensaje crítico')
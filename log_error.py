import logging
from typing import Optional

# configurar el registro
logging.basicConfig(filename='example.log', level=logging.DEBUG)

try:
    1/0
except Exception as e:
    logging.exception('Se produjo una excepción: %s', e)


from utils.create_folder_files import CreateFolderFile
from utils.custom_log import get_custom_logger


if __name__ == '__main__':
    create_folder = CreateFolderFile()
    success, location = create_folder.create_folder("c:\\hola")
    if success:
        print("Se logró crear la ruta")
    print(location)
    success_create_file, location_file = create_folder.create_file(location, "example.log")
    print(location_file)
    custom_logger = get_custom_logger(location_file)
    # ejemplo de registro
    custom_logger.debug('Este es un mensaje de depuración')
    custom_logger.info('Este es un mensaje de información')
    custom_logger.warning('Este es un mensaje de advertencia')
    custom_logger.error('Este es un mensaje de error')
    custom_logger.critical('Este es un mensaje crítico')
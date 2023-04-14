import os
from typing import Tuple, Optional

class CreateFolderFile:
    
    def create_folder(self, location: str = "") -> Tuple[bool, Optional[str]]:
        '''
        create a folder depending on the location passed
        if folder already exists simply avoid a error
        '''
        try:
            os.makedirs(location, exist_ok=True)
            return (True, location)
        except OSError as err:
            #raise OSError(f"An error to create the folder: ${err}")
            return (False, None)
        
    def create_file(self, folder: str = "", file_name: str = "") -> Tuple[bool, Optional[str]]:
        file_description_or_path = os.path.join(folder, file_name)
        if os.path.exists(file_description_or_path):
            return (False, file_description_or_path)
        with open(file_description_or_path, "w") as file:
            file.write("")
        return (True, file_description_or_path)
    

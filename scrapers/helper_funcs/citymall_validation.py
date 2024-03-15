## Do I need to write custom error for not able to access URL with requests

import re
from constants import CITYMALL_CATEGORYURL
class CityMallInputValidation:
    '''
    To validate user input data to be correct form.
    '''
    def __init__(self) -> None:
        pass
    
    def validate_category_url(self, input_category_url:str):
        ## Check w/ Starting Url
        if not input_category_url.startswith(CITYMALL_CATEGORYURL):
            raise ValueError("Input url isn't correct.")
        
        full_url_pattern = f"^{CITYMALL_CATEGORYURL}.*?\/c\/\w+$"
        if not re.match(full_url_pattern, input_category_url):
            raise ValueError("Input URL pattern is not correct.")
        
        '''
        ## Check it has correct sub_ids (But to get sub_ids , I need to have main_id first)
        last_sub_id = re.search(r"\/(\w+)$", input_category_url)[1]
        if last_sub_id not in sub_category_ids:
            ## Refactoring : should I use custom error 
            raise ValueError("Sub-category id is not found in std_sub_category_ids list.")
        '''
        return True
        
    
    def validate_available_category_name(self):
        ## category started with MU or SU can't be scraped.
        pass
        
        
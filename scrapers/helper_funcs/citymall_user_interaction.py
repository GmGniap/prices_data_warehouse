'''
Author : GmGniap
Start-date : March 12,2024
About : Helper script for CityMall Scraper + CLI app
Description : 
- This script will show options for the user to select to scrape. Can say user-interaction script.
- Main Category id will be the last 2-digits from the end of its url.
- Sub-category id will be the last 4-digits from the end its url
'''
from scrapers.citymall_scraper import CityMallCategoryScraper
from scrapers.helper_funcs.citymall_validation import CityMallInputValidation

class CityMallUserInteraction:
    def __init__(self) -> None:
        print("CityMall Scraper : Menu")
        print("Scraping main categories list ....")
        
        ## No sure to declare None first.
        # self.main_categories = None
        # self.sub_categories = None
        # self.selected_main = None
        # self.selected_sub = None
        
        self.inputValidator = CityMallInputValidation()
    
    @staticmethod
    def display_list_of_dictionary(input_list: list, id_key: str, title_key: str):
        ids = []
        print("-" * 25)
        for input_dict in input_list:
            print(f"{input_dict[id_key]} : {input_dict[title_key]}")
            ids.append(input_dict[id_key])
        print("-" * 25)
        return ids
        
    def display_main_categories(self):
        print("Here're list of main category id : title.")
        return self.display_list_of_dictionary(self.main_categories, "category_id", "category_title")

    def display_sub_categories(self, main_category_id):
        self.sub_categories = self.category_obj.get_sub_ids_under_main(main_category_id)
        return self.display_list_of_dictionary(self.sub_categories, "sub_category_id", "sub_category_title")
        
    def ask_main_input(self):
        self.main_ids = self.display_main_categories()
        self.selected_main = input("Enter category ID to select sub-categories >> ")
        while self.selected_main not in self.main_ids:
            print("You should type the correct category ID from given list!")
            self.selected_main = input("Re-enter correct category ID >> ")
        return self.selected_main
    
    def ask_sub_category_input(self):
        if self.ask_main_input():
            print("Finding related sub-categories ....")
            self.sub_ids = self.display_sub_categories(self.selected_main)
        self.selected_sub = input("Enter sub-category ID from above list >> ")
        while self.selected_sub not in self.sub_ids:
            print("You should type the correct category ID from given list!")
            self.selected_sub = input("Re-enter correct sub-category ID")
        return self.selected_sub
    
    ## Ask user to select action from 3 Options
    ## 1. Provide category_url to scrape - Need to check correct categorial url
    ## 2. Select category from menu
    ## 3. Scrape all - (shouldn't add before concurrency)
    def show_main_menu(self) -> None:
        print("Select number for below options. \
            \n[1] Provide category url to scrape. \
            \n[2] Select category from menu. \
            \n[3] Scrape all projects data. (Do not recommend!)")
    
    def ask_option1(self) -> None:
        print("Provide CORRECT category URL starting with https://....")
        option1_input_url = input("Paste link here >> ").lower()    ## Need to lower for some special cases
        try:
            self.inputValidator.validate_category_url(option1_input_url)
            print(f"Start scraping for correct URL : {option1_input_url}")
            return option1_input_url
        except ValueError as ve:
            print(f"Input URL doesn't look like correct. Error : {ve}")
            print("Retry to copy/paste correct URL!!")
            self.ask_option1()   
            
        ## if it's correct , can return matched category name
        ## After validating url , if it's correct result , I should confirm with selected category name and ask to continue 'y/n'

    def main_input_validate(self) -> int:
        try:
            main_menu_input = int(input("Enter selected number 1-3 >> "))
            if main_menu_input <= 0 and main_menu_input > 3:
                raise ValueError("Your input number is being out of scope.")
        except TypeError:
            print("You've to type only number between 1 to 3. Retry again.")
            self.main_input_validate()
        except ValueError:
            print("You've to select number between 1,2,3 options. Retry again.")
            self.main_input_validate()
        return main_menu_input

    def main_menu_selection(self, selected_num : int):
        if selected_num == 1:
            return self.ask_option1() ## Return correct url
        elif selected_num == 2:
            ## Need to get all main/sub categories list
            self.category_obj = CityMallCategoryScraper()
            self.main_categories = self.category_obj.get_main_category_ids()
            print("Option 2")
        elif selected_num == 3:
            print("Option 3")
        else:
            raise ValueError("Wrong number for option")
            
    def main_interaction(self):
        self.show_main_menu()
        main_user_input = self.main_input_validate()
        return self.main_menu_selection(main_user_input) ## Return correct url
        
            

    
    
    
                
                
            

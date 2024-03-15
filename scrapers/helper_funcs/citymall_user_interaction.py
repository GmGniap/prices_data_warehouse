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

class CityMallUserInteraction:
    def __init__(self) -> None:
        print("CityMall Scraper : Menu")
        print("Scraping main categories list ....")
        self.category_obj = CityMallCategoryScraper()
        self.main_categories = self.category_obj.get_main_category_ids()
        self.sub_categories = None
        self.selected_main = None
        self.selected_sub = None
    
    @staticmethod
    def display_list_of_dictionary(input_list):
        ids = []
        print("-" * 25)
        for input_dict in input_list:
            for id, title in input_dict.items():
                print(f"{id} : {title}")
                ids.append(id)
        print("-" * 25)
        return ids
        
    def display_main_categories(self):
        print("Here're list of main category id : title.")
        return self.display_list_of_dictionary(self.main_categories)

    def display_sub_categories(self, main_category_id):
        self.sub_categories = self.category_obj.get_sub_ids_under_main(main_category_id)
        print(f"Selected sub-categories under Category ID {main_category_id}")
        return self.display_list_of_dictionary(self.sub_categories)
        
    def ask_main_input(self):
        main_ids = self.display_main_categories()
        self.selected_main = input("Enter category ID to select sub-categories >> ")
        while self.selected_main not in main_ids:
            print("You should type the correct category ID from given list!")
            self.selected_main = input("Re-enter correct category ID >> ")
        return self.selected_main
    
    def ask_sub_category_input(self):
        if self.ask_main_input():
            print("Finding related sub-categories ....")
            sub_ids = self.display_sub_categories(self.selected_main)
        self.selected_sub = input("Enter sub-category ID from above list >> ")
        while self.selected_sub not in sub_ids:
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
        option1_input_url = input("Paste link here :: ")
        
        ## After validating url , if it's correct result , I should confirm with selected category name and ask to continue 'y/n'
    
    def main_input_validate(self) -> int:
        try:
            main_menu_input = int(input("Enter selected number 1-3 :: "))
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
            self.ask_option1()
            
    def main_interaction(self):
        self.show_main_menu()
        main_user_input = self.main_input_validate()
            

    
    
    
                
                
            

import cmd
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv(".env")  # Loads the .env file

URL = os.getenv("URL")

class ApiTestCLI(cmd.Cmd):
    intro = "Welcome to the Flask API Test CLI. Type 'help' or '?' to list commands.\n"
    prompt = "(API Test) "

    def __init__(self):
        super().__init__()
        self.base_url = URL

    def _print_response(self, response):
        """Pretty-print the HTTP response."""
        try:
            print(json.dumps(response.json(), indent=2))
        except ValueError:
            print(f"Response: {response.text}")

    def do_get_all_users(self, arg):
        """Fetch all users: get_all_users"""
        try:
            response = requests.get(f"{self.base_url}/users")
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")

    def do_get_user(self, arg):
        """Fetch a user by EDIPI: get_user <edipi>"""
        if not arg:
            print("Error: Please provide an EDIPI")
            return
        try:
            response = requests.get(f"{self.base_url}/users/{arg}")
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")

    def do_add_user(self, arg):
        """Add a new user: add_user"""
        print("Enter user details (press Enter to use default for optional fields):")
        rank = input("Rank: ")
        firstName = input("First Name: ")
        lastName = input("Last Name: ")
        mi = input("Middle Initial (optional): ")
        edipi = input("EDIPI (10 digits): ")
        dor = input("Date of Rank (YYYYMMDD): ")
        pmos = input("PMOS (4 digits): ")
        bilmos = input("BILMOS (4 digits): ")

        data = {
            "rank": rank.upper(),
            "firstName": firstName.upper(),
            "lastName": lastName.upper(),
            "mi": mi.upper() or "",
            "edipi": edipi,
            "dor": int(dor) if dor else 0,
            "pmos": pmos,
            "bilmos": bilmos
        }

        try:
            response = requests.post(f"{self.base_url}/users", json=data)
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")

    def do_update_user(self, arg):
        """Update a user by EDIPI: update_user <edipi>"""
        if not arg:
            print("Error: Please provide an EDIPI")
            return
        print(f"Enter updated details for user with EDIPI {arg}:")
        rank = input("Rank: ")
        firstName = input("First Name: ")
        lastName = input("Last Name: ")
        mi = input("Middle Initial (optional): ")
        dor = input("Date of Rank (YYYYMMDD): ")
        pmos = input("PMOS (4 digits): ")
        bilmos = input("BILMOS (4 digits): ")

        data = {
            "rank": rank,
            "firstName": firstName,
            "lastName": lastName,
            "mi": mi or "",
            "dor": int(dor) if dor else 0,
            "pmos": pmos,
            "bilmos": bilmos
        }

        try:
            response = requests.put(f"{self.base_url}/users/{arg}", json=data)
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")

    def do_delete_user(self, arg):
        """Delete a user by EDIPI: delete_user <edipi>"""
        if not arg:
            print("Error: Please provide an EDIPI")
            return
        try:
            response = requests.delete(f"{self.base_url}/users/{arg}")
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")
    def do_get_users_by_rank(self, arg):
        """Fetch all users by rank: get_users_by_rank <rank>"""
        if not arg:
            print("Error: Please provide a rank")
            return
        try:
            response = requests.get(f"{self.base_url}/users/rank/{arg}")
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")
    def do_get_users_by_mos(self, arg):
        """Fetch all users by bilmos: get_users_by_mos <bilmos>"""
        if not arg:
            print("Error: Please provide a bilmos")
            return
        try:
            response = requests.get(f"{self.base_url}/users/mos/{arg}")
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")
            
    def do_get_all_mos_desc(self, arg):
        """Fetch all mos descriptions: get_all_mos_desc"""
        try:
            response = requests.get(f"{self.base_url}/mos")
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")
    def do_get_mos_desc_by_bilmos(self, arg):
        """Fetch a mos description by bilmos: get_mos_desc_by_bilmos"""
        if not arg:
            print("Error: Please provide a bilmos")
            return
        try:
            response = requests.get(f"{self.base_url}/mos/{arg}")
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")
    def do_add_mos_desc(self, arg):
        """Add a new mos description: add_mos_desc"""
        print("Enter mos description details:")
        bilmos = input("BILMOS (4 digits): ")
        desc = input("Description: ")

        data = {
            "bilmos": bilmos,
            "desc": desc
        }

        try:
            response = requests.post(f"{self.base_url}/mos", json=data)
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")
    def do_update_mos_desc(self, arg):
        """Update a mos description by bilmos: update_mos_desc <bilmos>"""
        if not arg:
            print("Error: Please provide a bilmos")
            return
        print(f"Enter updated details for mos description with bilmos {arg}:")
        desc = input("Description: ")

        data = {
            "desc": desc
        }

        try:
            response = requests.put(f"{self.base_url}/mos/{arg}", json=data)
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")
    
    def do_delete_mos_desc(self, arg):
        """Delete a mos description by bilmos: delete_mos_desc <bilmos>"""
        if not arg:
            print("Error: Please provide a bilmos")
            return
        try:
            response = requests.delete(f"{self.base_url}/mos/{arg}")
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")
    
    def do_fill_counseling(self, arg):
        """Fill the counseling form: fill_counseling"""
        try:
            # Ask EDIPI of reported on
            edipi = "1631875455"
            # Ask EDIPI of senior
            senior_edipi = "1234567890"
            senior_billet = "safsdfsadfsag"
            # Fetch user
            response = requests.get(f"{self.base_url}/users/{edipi}")
            response.raise_for_status()
            user = response.json()
            
            # Fetch senior
            response = requests.get(f"{self.base_url}/users/{senior_edipi}")
            response.raise_for_status()
            senior = response.json()
            print(user)
            print(senior)
            # Ask for occasion
            occasion = "adafsdf"

            # Ask for PeriodFrom
            period_from = "asdf"

            # Ask for PeriodTo
            period_to = "asdfa"

            # Ask for topics
            topics = "safasfsa"
            
            # Ask for events
            events = "asfsdfa"
            
            # Ask for eval
            eval = "asdfsdfasdf"
            
            # Ask for goals
            goals = "afasdfsadf"
            
            # Ask for comments
            comments = "asfsafasdf"
            
            # Fetch MOS description
            response = requests.get(f"{self.base_url}/mos/{user.get('bilmos')}")
            response.raise_for_status()
            mos_desc = response.json()
            
            # Create JSON data
            
            data = {
                "EDIT_lastName": user.get('lastName'),
                "EDIT_firstName": user.get('firstName'),
                "Edit_MI": len(user.get('mi')) > 0 and user.get('mi') or "",
                "EDIT_EDIPI": user.get('edipi'),
                "EDIT_RANK": user.get('rank'),
                "EDIT_DOR": user.get('dor'),
                "EDIT_PMOS": user.get('pmos'),
                "EDIT_BILMOS": user.get('bilmos'),
                "EDIT_OCCASION": user.get('occasion'),
                "EDIT_perFrom": user.get('periodFrom'),
                "EDIT_perTo": user.get('periodTo'),
                "EDIT_sLastName": senior.get('lastName'),
                "EDIT_sFirstName": senior.get('firstName'),
                "EDIT_sMI": len(senior.get('mi')) > 0 and senior.get('mi') or "",
                "EDIT_sEDIPI": senior.get('edipi'),
                "EDIT_sRank": senior.get('rank'),
                "EDIT_Billet": senior.get('billet'),
                "EDIT_TOPICS": topics,
                "EDIT_EVENTS": events,
                "EDIT_mos": mos_desc.get('desc'),
                "EDIT_EVAL": eval,
                "EDIT_TASKS": goals,
                "EDIT_COMMENTS": comments
            }
           
            response=requests.post(f"{self.base_url}/fill_counseling", json=data)
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")


    def do_exit(self, arg):
        """Exit the CLI"""
        print("Goodbye!")
        return True

    def do_quit(self, arg):
        """Exit the CLI"""
        return self.do_exit(arg)
     
if __name__ == '__main__':
    ApiTestCLI().cmdloop()
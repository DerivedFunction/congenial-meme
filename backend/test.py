import cmd
import requests
import json

class ApiTestCLI(cmd.Cmd):
    intro = "Welcome to the Flask API Test CLI. Type 'help' or '?' to list commands.\n"
    prompt = "(API Test) "

    def __init__(self):
        super().__init__()
        self.base_url = "http://localhost:5000"

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
            response = requests.get(f"{self.base_url}/mosdesc")
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
            response = requests.get(f"{self.base_url}/mosdesc/{arg}")
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
            response = requests.post(f"{self.base_url}/mosdesc", json=data)
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
            response = requests.put(f"{self.base_url}/mosdesc/{arg}", json=data)
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
            response = requests.delete(f"{self.base_url}/mosdesc/{arg}")
            response.raise_for_status()
            self._print_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")
    
    def do_fill_counseling(self, arg):
        """Fill the counseling form: fill_counseling"""
        try:
            # Ask EDIPI of reported on
            edipi = input("Enter EDIPI of reported on: ")
            # Ask EDIPI of senior
            senior_edipi = input("Enter EDIPI of senior: ")

            
            response=requests.post(f"{self.base_url}/fill_counseling")
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
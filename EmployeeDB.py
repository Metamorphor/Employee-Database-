# Import the SQLite library
from sqlite3 import connect, OperationalError

# Create a connection object that represents the database
conn = connect('database.db')

# Cursor allows to Create sql commands
c = conn.cursor()

class Employee:
	"""Class takes all employee attributes and auto-generates company email address"""

	def __init__(self, id_num, title, first, last, salary):
		self.id_num = id_num
		self.title = title
		self.first = first
		self.last = last
		self.salary = salary

	@property
	def email(self):
		return f"{self.first.lower()}.{self.last.lower()}@abccompany.com"


class DataBaseOperations:
	"""All operations that create, add to, display, or amend the database"""
	
	@staticmethod
	def create_table():
		"""Create a table to hold all employee data."""       

		with conn:
			try:
				c.execute("""CREATE TABLE ABCemployees (
					id_num integer PRIMARY KEY,
					title text NOT NULL,
					first text NOT NULL,
					last text NOT NULL,
					email text NOT NULL,
					salary integer NOT NULL
					)""")
				print("\nThe table 'ABCemployees' has been created successfully")
			except OperationalError:
				print('\nThis table is already created')

	
	@staticmethod
	def insert_emp(emp):
		"""Insert a new employees details into the DB"""

		with conn:
			try:
				c.execute("INSERT INTO ABCemployees VALUES (:id_num, :title, :first, :last, :email, :salary)",
						  {'id_num': emp.id_num, 
							'title':   emp.title, 
							'first':   emp.first, 
							'last':    emp.last,
						  'email':   emp.email, 
							'salary':  emp.salary})
				print('\nNew employee created successfully\n')
			except Exception:
				print("\n***You must create an employee table first***")


	# SEARCHING THE DATABASE

	@staticmethod
	def create_display_headers(result):
		"""Creates headers for displayed data for readability"""

		if type(result) == type(tuple()):
			for index, detail in enumerate(result):
				if index == 0:
					print("\nEmployee ID: " + str(detail))
				elif index == 1:
					print("Employee Title: " + detail)
				elif index == 2:
					print("Employee Name: " + detail)
				elif index == 3:
					print("Employee Surname: " + detail)
				elif index == 4:
					print("Employee Email: " + detail)
				elif index == 5:
					print("Employee Salary: £" + str(detail))
		else:
			return None
							

	@staticmethod
	def get_emp_by_name(lastname):
		"""Extract data from all employees with a particular last name"""

		# Note: SELECT statements do not need to be committed like UPDATE, INSERT, DELETE
		try:
			c.execute("SELECT * FROM ABCemployees WHERE last=:last", {'last': lastname})
			return c.fetchall()
		except sqlite3.error as e:
			return None

	
	@staticmethod
	def get_emp_by_id(id_num):
		"""Extract an employees details from their ID number only"""

		try:
			c.execute("SELECT * FROM ABCemployees WHERE id_num=:id_num", {'id_num': id_num})
			return c.fetchone()
		except sqlite3.error as e:
			return None

   
	@staticmethod
	def get_emp_by_salary(salary):
		"""Extract all employees data who earn a specific salary"""

		try:
			c.execute("SELECT * FROM ABCemployees WHERE salary=:salary", {'salary': salary})
			return c.fetchall()
		except sqlite3.error as e:
			return None

   
	@staticmethod
	def display_database():
		"""Display the entire database in raw tuple format"""

		try:
			c.execute("SELECT * FROM ABCemployees")
			result = c.fetchall()
			print('\nABCemployees:\n')
			for i in result:
				print(i, "\n")
		except sqlite3.error as e:
			print(e)

   
	@staticmethod
	def get_email_by_id(id_num):
		"""Get an employees EMAIL from their ID"""

		try:
			c.execute("SELECT email FROM ABCemployees WHERE id_num=:id_num", {'id_num': id_num})
			result = c.fetchone()
			return result[0]
		except sqlite3.error as e:
			return None


	# UPDATING THE DATABASE
   
	@staticmethod
	def update_salary(id_num, salary):
		"""Update an employees Salary"""

		with conn:
			try:
				c.execute("""UPDATE ABCemployees SET salary = :salary WHERE id_num = :id_num""",
						  {'id_num': id_num, 'salary': salary})
			except sqlite3.error as e:
				return None

   
	@staticmethod
	def update_firstname(id_num, first):
		"""Update an employees firstname"""

		with conn:
			try:
				c.execute("""UPDATE ABCemployees SET first = :first WHERE id_num = :id_num""",
						  {'id_num': id_num, 'first': first})
			except sqlite3.error as e:
				return None

	
	@staticmethod
	def update_surname(id_num, last):
		"""Update an employees firstname"""

		with conn:
			try:
				c.execute("""UPDATE ABCemployees SET last = :last WHERE id_num = :id_num""",
						  {'id_num': id_num, 'last': last})
			except sqlite3.error as e:
				return None

	
	@staticmethod
	def update_email(id_num, email):
		"""Update an employees email address"""

		with conn:
			try:
				c.execute("""UPDATE ABCemployees SET email = :email WHERE id_num = :id_num""",
						  {'id_num': id_num, 'email': email})
			except sqlite3.error as e:
				return None


	# DELETING ENTRIES
   
	@staticmethod
	def remove_emp(id_num):
		"""Remove a complete employee entry"""

		with conn:
			try:
				c.execute("DELETE from ABCemployees WHERE id_num = :id_num",
						  {'id_num': id_num})
			except sqlite3.error as e:
				return None


class UserMenu:
	"""Class contains all user displayed menus and deals with user inputs"""

	@staticmethod
	def new_emp_input():
		"""Take inputs from admin to populate new employee entry"""

		print("Company emails and employee ID's are generated automatically\n")
		id_num = None 
		first = input('Enter first name: ')
		last = input('Enter surname: ')
		title = input('Enter title (ie: Mr/Mrs/Prof): ')
		salary = input('Enter salary: ')
		emp = Employee(id_num, title, first, last, salary)
		DataBaseOperations.insert_emp(emp)

    
	@staticmethod
	def remove_emp_input():
		"""Take inputs from admin to allow employee removal"""

		print('You have chosen to permanently remove an employees details from the database ')
		print('\n'"""Would you like to proceed?
		1 - Yes
		2 - No, return to main menu!""")

		user_choice = input('Enter your selection: ')
		if user_choice == '1':
			id_num = UserMenu.search_by_id_inputs()
			print("""\nIs the above record the correct one to delete?
			1 - Yes
			2 - No, return me to the menu!""")
			inp = input("Enter your selection: ")
			if inp == '1':
				DataBaseOperations.remove_emp(id_num)
				print("\nEmployee Removed ")
			elif inp == '2':
				UserMenu.remove_emp_input()
			else:
				print("***Incorrect Selection***\n")
				UserMenu.main_menu()		
		else:
			UserMenu.main_menu()


	# USER INPUTS FOR UPDATE REQUESTS

	
	@staticmethod
	def update_firstname_inputs():
		"""Take inputs from admin to update first name"""

		id_num = UserMenu.search_by_id_inputs()
		first = input('\nEnter updated firstname: ')
		DataBaseOperations.update_firstname(id_num, first)
		print("\nUpdate successful: ")
		DataBaseOperations.create_display_headers(DataBaseOperations.get_emp_by_id(id_num))
		UserMenu.update_menu()

    
	@staticmethod
	def update_surname_inputs():
		"""Take inputs from admin to update surname"""

		id_num = UserMenu.search_by_id_inputs()
		last = input('\nEnter updated surname: ')
		DataBaseOperations.update_surname(id_num, last)
		print("\nUpdate successful: ")
		DataBaseOperations.create_display_headers(DataBaseOperations.get_emp_by_id(id_num))
		UserMenu.update_menu()

    
	@staticmethod
	def update_salary_inputs():
		"""Take inputs from admin to update Salary"""

		id_num = UserMenu.search_by_id_inputs()
		salary = input('\nEnter updated salary: ')
		DataBaseOperations.update_salary(id_num, salary)
		print("\nUpdate successful: ")
		DataBaseOperations.create_display_headers(DataBaseOperations.get_emp_by_id(id_num))
		UserMenu.update_menu()

	# Complete	
	@staticmethod
	def update_email_inputs():
		"""Take inputs from admin to update email"""

		print("""Company emails should be of the form 'firstname.surname@ABCcompany'""")
		id_num = UserMenu.search_by_id_inputs()
		first = input('\nEnter new email Firstname: ')
		last = input('\nEnter new email Surname: ')
		email = first + '.' + last + '@abccompany.com'
		DataBaseOperations.update_email(id_num, email)
		print("\nUpdate successful: ")
		DataBaseOperations.create_display_headers(DataBaseOperations.get_emp_by_id(id_num))
		UserMenu.update_menu()

	# USER INPUT FROM SEARCH REQUESTS
   	
	@staticmethod
	def search_by_id_inputs():
		"""Take inputs from admin to search by ID"""

		id_num = input('\nEnter employees ID number: ')
		if DataBaseOperations.get_emp_by_id(id_num) == None:
			print("\nNo record of this ID number exists")
			UserMenu.main_menu()
		else:
			DataBaseOperations.create_display_headers(DataBaseOperations.get_emp_by_id(id_num))
			return id_num

    
	@staticmethod
	def search_by_surname_inputs():
		"""Take inputs from admin to search by Surname"""

		last = input('\nEnter employee surname: ')
		if DataBaseOperations.get_emp_by_name(last) == None or DataBaseOperations.get_emp_by_name(last) == []:
			print("\nNo record of this surname exists")
			UserMenu.search_menu()
		else:
			result = DataBaseOperations.get_emp_by_name(last)
			for i in result:
					DataBaseOperations.create_display_headers(i)
			UserMenu.search_menu()

	
	@staticmethod
	def search_by_salary_inputs():
		"""Take inputs from admin to search by salary"""

		salary = input('\nEnter salary: ')
		if DataBaseOperations.get_emp_by_salary(salary) == None or DataBaseOperations.get_emp_by_salary(salary) == []:
			print("\nNo record of this salary level exists")
			UserMenu.search_menu()
		else:
			result = DataBaseOperations.get_emp_by_salary(salary)
			for i in result:
					DataBaseOperations.create_display_headers(i)
			UserMenu.search_menu()

	
	@staticmethod
	def get_email_inputs():
		"""Take inputs from admin to obtain email address for a particular user ID"""

		id_num = input('\nEnter Employee ID number: ')
		if DataBaseOperations.get_emp_by_id(id_num) == None:
			print("\nNo record of this ID number exists")
			UserMenu.search_menu()
		else:
			print("Employee Email: ", DataBaseOperations.get_email_by_id(id_num))
			UserMenu.search_menu()

	# USER MENU's
  
	@staticmethod
	def search_menu():
		"""Secondary menu for search queries"""

		while True:
			input('\nPress enter to continue to the search menu: ')
			print('\n'"""How would you like to search?
			1 - By employee ID
			2 - By employee Surname
			3 - By Salary
			4 - Display the whole database
			5 - Get email address from an employee ID
			6 - Return to the main menu""")
			search = input('\nEnter your selection: ')
			if search == '1':
				UserMenu.search_by_id_inputs()
			elif search == '2':
				UserMenu.search_by_surname_inputs()
			elif search == '3':
				UserMenu.search_by_salary_inputs()
			elif search == '4':
				DataBaseOperations.display_database()
			elif search == '5':
				UserMenu.get_email_inputs()
			elif search == '6':
				UserMenu.main_menu()
			else:
				print('\n***Incorrect Selection***')
				continue

   
	@staticmethod
	def update_menu():
		"""Secondary menu for update queries"""

		while True:
			input('\nPress enter to continue to the update menu: ')
			print('\n'"""What would you like to update?
			NOTE: emails will NOT be updated automatically with name changes
		
			1 - Employee First Name
			2 - Employee Surname
			3 - Employee Salary
			4 - Employee Email
			5 - Return to the main menu""")

			user_choice = input('Enter your selection: ')	
			if user_choice == '1':
				UserMenu.update_firstname_inputs()
			elif user_choice == '2':
				UserMenu.update_surname_inputs()
			elif user_choice == '3':
				UserMenu.update_salary_inputs()
			elif user_choice == '4':
				UserMenu.update_email_inputs()
			elif user_choice == '5':
				UserMenu.main_menu()
			else:
				print('\n***Incorrect Selection***')
				continue

	@staticmethod
	def main_menu():
		"""Main user interface"""

		while True:
			print(" ")
			input('\nPress enter to continue to the main menu: ')
			print('\nWelcome to ABC Company database menu')
			print("""
			Please choose from the following options:
			1 - Create an employee table
			2 - Insert a new employee
			3 - Remove an existing employee
			4 - Update an employees details
			5 - Search the database
			6 - Display the entire employee database
			""")

			user_choice = input('Enter your selection: ')
			if user_choice == '1':
				DataBaseOperations.create_table()
			elif user_choice == '2':
				UserMenu.new_emp_input()
			elif user_choice == '3':
				UserMenu.remove_emp_input()
			elif user_choice == '4':
				UserMenu.update_menu()
			elif user_choice == '5':
				UserMenu.search_menu()
			elif user_choice == '6':
				DataBaseOperations.display_database()
			else:
				print('\n***Incorrect Selection***')
				continue


# Initialise the program
UserMenu.main_menu()

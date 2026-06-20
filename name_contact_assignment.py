# Contact Management System

contacts = []

# Validation Functions
def valid_phone(phone):
    for char in phone:
        if not (char.isdigit() or char == "-" or char == "+"):
            return False
    return True


def valid_email(email):
    if email == "":
        return True
    return "@" in email and "." in email

# CRUD Functions
def add_contact():
    name = input("Enter Name: ")
    phone = input("Enter Phone Number: ")
    email = input("Enter Email: ")

    if not valid_phone(phone):
        print("Error: Invalid phone number!")
        return

    if not valid_email(email):
        print("Error: Invalid email address!")
        return

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email
    })

    print("Contact added successfully.")

def view_contact():
    name = input("Enter name to view: ")

    for contact in contacts:
        if contact["name"].lower() == name.lower():
            print("\nContact Found")
            print("Name :", contact["name"])
            print("Phone:", contact["phone"])
            print("Email:", contact["email"])
            return

    print("Contact not found.")

def update_contact():
    name = input("Enter contact name to update: ")

    for contact in contacts:
        if contact["name"].lower() == name.lower():

            new_name = input("New Name: ")
            new_phone = input("New Phone: ")
            new_email = input("New Email: ")

            if not valid_phone(new_phone):
                print("Error: Invalid phone number!")
                return

            if not valid_email(new_email):
                print("Error: Invalid email!")
                return

            contact["name"] = new_name
            contact["phone"] = new_phone
            contact["email"] = new_email

            print("Contact updated successfully.")
            return

    print("Contact not found.")

def delete_contact():
    name = input("Enter contact name to delete: ")

    for contact in contacts:
        if contact["name"].lower() == name.lower():
            contacts.remove(contact)
            print("Contact deleted successfully.")
            return

    print("Contact not found.")

# Search Function
def search_contacts():
    keyword = input("Enter name, phone or email to search: ").lower()

    results = []

    for contact in contacts:
        if (keyword in contact["name"].lower() or
                keyword in contact["phone"].lower() or
                keyword in contact["email"].lower()):
            results.append(contact)

    if results:
        print("\nSearch Results")
        print("-" * 40)

        for contact in results:
            print("Name :", contact["name"])
            print("Phone:", contact["phone"])
            print("Email:", contact["email"])
            print("-" * 40)
    else:
        print("No matching contacts found.")

# List of Contacts
def list_contacts():
    if not contacts:
        print("No contacts available.")
        return

    print("\nAll Contacts")
    print("-" * 40)

    for contact in contacts:
        print("Name :", contact["name"])
        print("Phone:", contact["phone"])
        print("Email:", contact["email"])
        print("-" * 40)

# The Main Menu
def main():
    while True:

        print("\n=== Contact Manager Menu ===")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Search Contacts")
        print("6. List All Contacts")
        print("7. Exit")

        choice = input("Choose an option (1-7): ")

        if choice == "1":
            add_contact()

        elif choice == "2":
            view_contact()

        elif choice == "3":
            update_contact()

        elif choice == "4":
            delete_contact()

        elif choice == "5":
            search_contacts()

        elif choice == "6":
            list_contacts()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-7.")


# Run Program
main()
from infraction import Infraction, InfractionValueError


def main_menu():
    while True:
        print("\n--- CAR MANAGEMENT SYSTEM: INFRACTIONS ---")
        print("1. Display All Infractions")
        print("2. Add New Infraction")
        print("3. Search Infraction")
        print("4. Update Infraction")
        print("5. Delete Infraction")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        try:
            if choice == "1":
                Infraction.display_existing_infraction()
            elif choice == "2":
                desc = input("Enter description: ")
                price = float(input("Enter fine price: "))
                inf = Infraction(desc, price)
                inf.save()
            elif choice == "3":
                term = input("Enter search keyword: ")
                results = Infraction.search_infraction(term)
                for r in results:
                    print(r)
            elif choice == "4":
                Infraction.update_infraction()
            elif choice == "5":
                Infraction.delete_infraction()
            elif choice == "6":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except Exception as e:
            print(f"Error: {e}")

# main program:


main_menu()

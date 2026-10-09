from db import connection


class InfractionValueError(Exception):
    pass


class InfractionDeleteError(Exception):
    pass


class Infraction:
    def __init__(self, description: str, fine_price: float):
        self.__description = description
        self.__fine_price = fine_price

    def is_valid(self) -> bool:  # checks if infraction objects are valid
        if self.__description == "":
            if self.__fine_price > 0:
                return True
        return False

    def save(self):
        if not self.is_valid():
            raise InfractionValueError("Invalid Infraction Properties")
        else:
            if Infraction.check_description_exist(self.__description):
                raise InfractionValueError("Invalid Infraction Description. Already exist")
            query = """
                INSERT INTO infraction(description,fine_price)
                VALUES(%s, %s)
            """
            cursor = connection.cursor()
            cursor.execute(query, (self.__description, self.__fine_price))
            connection.commit()
            cursor.close()
            print("Infraction Added Successfully")

    @classmethod
    def check_description_exist(cls, description) -> bool:
        query = """
            SELECT *
            FROM infraction
            WHERE description = %s
        """
        cursor = connection.cursor()
        cursor.execute(query, (description,))
        infraction = cursor.fetchone()
        cursor.close()
        return True if infraction else False

    @classmethod
    def display_existing_infraction(cls) -> list:
        query = """
            SELECT *
            FROM infraction
        """
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchone()
        if rows:
            print(" ID NAME  PRICE")
            print("================")
            while rows:
                print(rows[0], rows[1], rows[2])
                rows = cursor.fetchone()
            cursor.close()
        else:
            print("No infractions found")

    # searches an infraction using the id or description returns data
    @classmethod
    def search_infraction(cls, description: str):
        query = """
            SELECT * 
            FROM infraction
            WHERE description LIKE %s
        """
        cursor = connection.cursor()
        cursor.execute(query, (description,))
        infractions = cursor.fetchall()
        cursor.close()
        return infractions

    @classmethod
    def delete_infraction(cls):
        cls.display_existing_infraction()
        print("WHICH INFRACTION DO YOU WANT TO DELETE?")
        try:
            infraction_id = int(input("Enter the infraction's id: "))
        except ValueError:
            raise InfractionValueError("IT SHOULD BE INTEGER")

        exists = cls.valid_id(infraction_id)
        if not exists:
            raise InfractionValueError("Infraction does not exist")

        print("ARE YOU SURE?")
        validating = input("(YES or NO) =>").strip().upper()
        if validating == "YES":
            cursor = connection.cursor()
            query = """
            DELETE *
            FROM infraction
            WHERE id = %s;
            """
            cursor.execute(query, (infraction_id,))
            cursor.close()
            cls.display_existing_infraction()

    @classmethod
    def valid_description(cls, new_description) -> bool:
        if new_description == "":
            return False
        if cls.search_infraction(new_description):
            return False
        return True

    @classmethod
    def valid_id(cls, infraction_id: int) -> bool:
        query = """
            SELECT id 
            FROM infraction
            WHERE id = %s
        """
        cursor = connection.cursor()
        cursor.execute(query, (infraction_id,))
        infraction = cursor.fetchone()
        cursor.close()
        if infraction:
            return True
        return False

    @classmethod
    def valid_fine_price(cls, new_fine_price) -> bool:
        if new_fine_price > 0:
            return True
        return False

    @classmethod
    def update_infraction(cls):
        Infraction.display_existing_infraction()
        infraction_id = int(input("Enter an id here: "))
        if Infraction.valid_id(infraction_id):
            new_description = input("Enter new description: ")
            new_fine_price = float(input("Enter new fine price: "))
            if Infraction.valid_description(new_description):
                query = """
                    UPDATE infraction
                    SET description = %s
                    WHERE id = %s
                """
                cursor = connection.cursor()
                cursor.execute(query, (new_description, infraction_id))
                connection.commit()
                cursor.close()
                print("Update done successfully!")
            else:
                raise InfractionValueError("Description cannot be empty or already existing")
            if Infraction.valid_fine_price(new_fine_price):
                query = """
                    UPDATE infraction
                    SET fine_price = %s
                    WHERE id = %s
                """
                cursor = connection.cursor()
                cursor.execute(query, (new_fine_price, infraction_id))
                connection.commit()
                cursor.close()
                print("Fine price added successfully!")
            else:
                raise InfractionValueError("Fine price must be greater than zero")
        else:
            raise InfractionValueError("ID cannot be found")


that_infraction = Infraction("Driving with no lights on", 8000)
Infraction.update_infraction()

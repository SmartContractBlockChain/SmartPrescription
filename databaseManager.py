def format_list(results):
    formatted_list = []

    for result in results:
        formatted_list.append(result[0].rstrip())

    return formatted_list


class DataBaseManager:

    def __init__(self, mysql):
        self.mysql_client = mysql

    def get_user_address(self, name, surname, user_type):
        cur = self.mysql_client.connection.cursor()
        cur.execute(
            "SELECT blockchainAddress FROM users"
            " WHERE users.name = %s AND users.surname = %s AND users.userType = %s", [name, surname, user_type])
        address = cur.fetchone()
        cur.close()

        return address[0]

    def get_prescriptions_by_type(self, name, surname, user_type):
        if user_type == 'Doctor':
            cur = self.mysql_client.connection.cursor()
            cur.execute(
                "SELECT address FROM users JOIN prescriptions ON doctor_id = users.id WHERE users.name = %s and "
                "surname = %s and userType = %s", [name, surname, user_type])

            prescriptions = cur.fetchall()
            cur.close()

            return format_list(prescriptions)
        elif user_type == 'Pharmacist':
            cur = self.mysql_client.connection.cursor()
            cur.execute(
                "SELECT address FROM users JOIN prescriptions ON pharmacist_id = users.id WHERE users.name = ? and "
                "surname = ? and userType = ?", name, surname, user_type)

            prescriptions = cur.fetchall()
            cur.close()

            return format_list(prescriptions)
        else:
            return []

    def get_all_pharmacists_addresses(self):
        cur = self.mysql_client.connection.cursor()
        cur.execute("SELECT blockchainAddress FROM users WHERE users.userType = %s", ['Pharmacist'])
        pharmacists_addresses = cur.fetchall()
        cur.close()

        return format_list(pharmacists_addresses)

    def save_prescription(self, prescription_address, doctor_account, patient_account):
        doctor_id = self.get_user_id_by_address(doctor_account)
        patient_id = self.get_user_id_by_address(patient_account)

        cur = self.mysql_client.connection.cursor()
        cur.execute("INSERT INTO prescriptions(address, doctor_id, patient_id) VALUES (%s,%s,%s)",
                    [prescription_address, doctor_id, patient_id])

        self.mysql_client.connection.commit()
        cur.close()

    def get_user_id_by_address(self, user_account):
        cur = self.mysql_client.connection.cursor()
        cur.execute("SELECT id FROM users WHERE users.blockchainAddress = %s", [user_account])
        user_id = cur.fetchone()
        cur.close()

        return user_id[0]

    # TODO finish this function
    def set_pharmacist_in_contract(self, pharmacist_address, prescription_address):
        pharmacist_id = self.get_user_id_by_address(pharmacist_address)



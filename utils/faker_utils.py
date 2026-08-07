from faker import Faker

fake = Faker()


def get_user_data():
    return {
        "name": fake.name(),
        "username": fake.user_name(),
        "email": fake.email()
    }
from faker import Faker
from gender_guesser.detector import Detector

faker = Faker()
# faker.add_provider("faker.providers.job")

a = []
for i in range(10):
    a.append(faker.name())

# Пример использования
print(a)
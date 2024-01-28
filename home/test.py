from gender_guesser.detector import Detector


def get_gender(name):
    d = Detector()
    gender = d.get_gender(name)

    if gender == "unknown":
        print(f"Unable to determine the gender of {name}.")
    else:
        print(f"The gender of {name} is {gender}.")


# Пример использования
get_gender("John")
get_gender("Maria")
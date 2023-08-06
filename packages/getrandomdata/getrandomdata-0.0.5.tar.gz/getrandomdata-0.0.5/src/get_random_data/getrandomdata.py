"""
Python script to generate csv with random data. 

Random data here can be some pre-made set of lists that hold some entities.
Then, we can pick random elements from the lists and create a randomly mix-matched row for the csv. 

"""
import random

# define the list of entities to be used
names = ["carlo","basheer","john","valentina","kriss","jose","rahul","albert","jason","george","krishna","simran","jenny","rebecca","khloe","toro","shin"]
countries = ["india","usa","australia","japan","china","germany","spain","italy"]
ages = [age for age in range(22,50)]
occupations = ["software tester","project manager","technical lead","quality manager","marketing head","content creator","editor","associate engineer"]
mail_providers = ["gmail.com","yahoo.com","hotmail.com"]
house_no = [number for number in range(1,1000,20)] 
kids = ["Y","N"]
licence = ["Y","N"]


# generate a row with randomly picked values for each column
def generateRow(names=names,countries=countries,ages=ages,occupations=occupations,mail_providers=mail_providers,house_no=house_no,kids=kids,licence=licence):
    name = random.choice(names)

    random_dict = {
        "name" : name,
        "email" : f"{name}{random.choice(ages)}@{random.choice(mail_providers)}",
        "country" : random.choice(countries),
        "occupation" : random.choice(occupations),
        "house_no" : random.choice(house_no),
        "kids" : random.choice(kids),
        "lincense" : random.choice(licence)
    }

    return random_dict







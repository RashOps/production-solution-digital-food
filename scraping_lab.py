import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.infocalories.fr/calories/calories-abricot-fruit.php")
soup = BeautifulSoup(response.content, "html.parser")

if response.status_code == 200:
    print(f"Site fonctionnel: {response.status_code}")
else: 
    print(f"Erreur: {response.status_code}")

# Get the whole content of the page ----------------------
print(soup.prettify())

# Find the title - aliment name ---------------------
h1 = soup.find("h1").get_text()
aliment = h1.split(" ")[-1]

# Find the calories --------------------------------
characteristics = soup.find("div", id="diva").find_all("b")
# print(characteristics)
calories = characteristics[0].get_text()
proteins = characteristics[1].get_text()
carbs = characteristics[2].get_text()
fat = characteristics[3].get_text()

def retrieve_food_infos(food_name):
    def get_url(food_name):
        """ function : get the URL of the food given its name """
        url_1 = f"https://www.infocalories.fr/calories/calories-{food_name}-fruit.php"
        url_2 = f"https://www.infocalories.fr/calories/calories-{food_name}.php"

        response_1 = requests.get(url_1)
        response_2 = requests.get(url_2)

        return url_1 if response_1.status_code == 200 else url_2
    
    url = get_url(food_name)
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Site fonctionnel: {response.status_code}")
    else: 
        raise Exception(f"Erreur: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")

    # Aliment name
    h1 = soup.find("h1").get_text()
    aliment = h1.split(" ")[-1]

    # Find aliment characteristics
    characteristics = soup.find("div", id="diva").find_all("b")
    calories = characteristics[0].get_text()
    proteins = characteristics[1].get_text()
    carbs = characteristics[2].get_text()
    fat = characteristics[3].get_text()

    return aliment, calories, proteins, carbs, fat

if __name__ == "__main__":
    food_name = input("Enter the name of the food: ")
    aliment, calories, proteins, carbs, fat = retrieve_food_infos(food_name)
    print(f"Aliment: {aliment}")
    print(f"Calories: {calories}")
    print(f"Proteins: {proteins}")
    print(f"Carbs: {carbs}")
    print(f"Fat: {fat}")
import requests
from bs4 import BeautifulSoup

class Food:
    """ class food """
    __name = None
    __calories = None
    __fat = None
    __carbs = None
    __proteins = None

    def get_name(self):
        """ function : get the food name """
        return self.__name

    def set_name(self,name):
        """ function : set the food name """
        self.__name = name

    def get_calories(self):
        """ function : get the property named calories of the food """
        return self.__calories
        

    def set_calories(self,calories):
        """ function : set the property named calories of the food """
        self.__calories = calories

    def get_fat(self):
        """ function : get the property named fat of the food """
        return self.__fat

    def set_fat(self,fat):
        """ function : set the property named fat of the food """
        self.__fat = fat

    def get_carbs(self):
        """ function : get the property named carbs of the food """
        return self.__carbs

    def set_carbs(self,carbs):
        """ function : set the property named carbs of the food """
        self.__carbs = carbs

    def get_proteins(self):
        """ function : get the property named proteins of the food """
        return self.__proteins

    def set_proteins(self,proteins):
        """ function : set the property named proteins of the food """
        self.__proteins = proteins

    def retrieve_food_infos(self,food_name):
        """ function : scrap the properties of the food from a website given its name
        
        - think of making the URL a global variable
        - check whether the request succeed before trying to parse the payload
        - if not succesfull, raise an error
        
        """
        """ function : get the URL of the food given its name """
        def get_url(food_name):
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
        self._calories = characteristics[0].get_text()
        self._proteins = characteristics[1].get_text()
        self._carbs = characteristics[2].get_text()
        self._fat = characteristics[3].get_text()
        self._name = aliment


        return self._calories, self._proteins, self._carbs, self._fat, self._name
        

    def display_food_infos(self):
        """ function : display the properties of the food 
        the outlook should be similar to this:
                ------------------------------------------------
                name	    calories	fat	    carbs	proteins
                tomate	    21.0		0.3	    4.6	    0.8
                ------------------------------------------------
        """
        print(f"{'name':<10} {'calories':<10} {'fat':<10} {'carbs':<10} {'proteins':<10}")
        print("-" * 50)
        print(f"{self._name:<10} {self._calories:<10} {self._fat:<10} {self._carbs:<10} {self._proteins:<10}")

    
    def save_to_csv_file(self, file_name):
        """ function : save the properties of the food in a csv file 
        - use function with for file opening
        """
        with open(file_name, 'a') as file:
            file.write(f"name,calories,fat,carbs,proteins\n")
            file.write(f"{self._name},{self._calories},{self._fat},{self._carbs},{self._proteins}\n")


    def is_fat(self):
        """ function : return true or false whether the food has more than 20% of fat 
        - define a fat threshold and write the function accordingly
        """
        fat_threshold = 20
        return float(self._fat) > fat_threshold
        
if __name__ == "__main__":
    food = Food()
    food.retrieve_food_infos("tomate")
    food.display_food_infos()
    food.save_to_csv_file("food.csv")
    print(food.is_fat())
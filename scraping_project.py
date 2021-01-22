#Grabing data from http://quotes.toscrape.com
#After obtaining the data, I will create a guessing game
from bs4 import BeautifulSoup
import requests
from random import choices

site_url = "http://quotes.toscrape.com/"

#Function to find the next page of quotes:
def find_next_page(parse_file):
	next_part = parse_file.select(".next")
	if next_part == []:
		return None
	node = parse_file.select(".next")[0]
	partial_url = node.find("a")["href"]
	full_next_url = site_url + partial_url[1:]
	return full_next_url

#Function to get the current page quotes:
def get_page_results(web_url): 
	html_file = requests.get(web_url)
	parse_file = BeautifulSoup(html_file.text, "html.parser")
	quote_URL = parse_file.find_all(class_ = "quote")
	for item in quote_URL:
		quote_url = item.find("a")['href']
		quote_url = site_url + quote_url[1:]
		author_name = item.find(class_ = "author").get_text()
		quote_text = item.find(class_ = "text").get_text()
		quote_entries.append([author_name, quote_text, quote_url])
	next_url = find_next_page(parse_file)
	return next_url

#Function to call to get results and to check for the end of the pages:
def get_website_data(web_url):
	while web_url != None:
		web_url = get_page_results(web_url)

#Function for incorrect guesses:
def incorrect_guess():
	print("Incorrect guess!")
	print("Here is a hint:")

#Function to get a list for author hints
def get_hints(rand_quote):
	hint_html = requests.get(rand_quote[2])
	hint_parsed = BeautifulSoup(hint_html.text, "html.parser")
	birth_year = hint_parsed.find(class_ = "author-born-date").get_text()
	birth_location = hint_parsed.find(class_ = "author-born-location").get_text()
	author_name = rand_quote[0].split()
	hints = [f"Birth Year: {birth_year}", 
	f"Birth Location: {birth_location}", 
	f"First letter of first name: {author_name[0][0]}",
	f"First letter of Letter name: {author_name[1][0]}"]
	return hints

quote_entries = []
get_website_data(site_url)

#Set up the game:
play_again = "yes"
#Loop for game:
while play_again in ('yes', 'y'):
	random_quote = choices(quote_entries)[0]
	author_name = random_quote[0].lower()
	print(f"{random_quote[1]}")
	hint_list = get_hints(random_quote)
	guess_name = input("Who said this quote? ").lower()
	for i in hint_list:
		if guess_name != author_name:
			incorrect_guess()
			print(i)
			guess_name = input("Try again: ")
		else:
			break
	if guess_name == author_name:
		print("You guessed correctly!")
		play_again = input("Would you like to play again?(yes/no) ").lower()
	else: 
		print(f"Sorry! The correct name is {author_name}")
		play_again = input("Would you like to play again?(yes/no) ").lower()

print("Thanks for playing!")
		


		
	




 











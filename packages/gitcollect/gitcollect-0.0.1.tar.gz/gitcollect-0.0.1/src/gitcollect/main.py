from bs4 import BeautifulSoup
import requests
  
def repo_desc():
  """
  Gets the repo's description
  """
  rl = input("repo link? ")
  page = requests.get(rl)
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find(class_="f4 my-3").get_text()
  print(e)

def repo_stargazers():
  """
  Gets the number of stargazers
  """
  rl = input("repo link? ")
  page = requests.get(f"{rl}")
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find(class_="Counter js-social-count").get_text()
  print(e)

def issues_open():
  """
  Gets the number of issues open
  """
  rl = input("repo link? ")
  page = requests.get(f"{rl}")
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find_all(class_='Counter')[3].get_text()
  print(e)

def pr_open():
  """
  Gets the number of pull requests open
  """
  rl = input("repo link? ")
  page = requests.get(f"{rl}")
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find_all(class_='Counter')[4].get_text()
  print(e)
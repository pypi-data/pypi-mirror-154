from bs4 import BeautifulSoup
import requests
  
def repo_desc(repo_link):
  """
  Gets the repo's description
  """
  page = requests.get(repo_link)
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find(class_="f4 my-3").get_text()
  print(e)

def repo_stargazers(repo_link):
  """
  Gets the number of stargazers
  """
  page = requests.get(repo_link)
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find(class_="Counter js-social-count").get_text()
  print(f"{e} stargazers ⭐")

def issues_open(repo_link):
  """
  Gets the number of issues open
  """
  page = requests.get(repo_link)
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find_all(class_='Counter')[3].get_text()
  print(f"{e} issues open 🟢")

def issues_closed(repo_link):
  """
  Gets the number of issues open
  """
  if repo_link.endswith("/"):
    page = requests.get(f"{repo_link}issues?q=is%3Aissue+is%3Aclosed") #hmmm
  else:
    page = requests.get(f"{repo_link}/issues?q=is%3Aissue+is%3Aclosed")
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find(class_='btn-link selected').get_text()
  print(f"{e} (issues) 🔴") #don't know why there's so many blank space hmmmm


def pr_open(repo_link):
  """
  Gets the number of pull requests open
  """
  page = requests.get(repo_link)
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find_all(class_='Counter')[4].get_text()
  print(f"{e} pull requests open 🟩")

def pr_closed(repo_link):
  """
  Gets the number of pull requests open
  """
  if repo_link.endswith("/"):
    page = requests.get(f"{repo_link}pulls?q=is%3Apr+is%3Aclosed")
  else:
    page = requests.get(f"{repo_link}/pulls?q=is%3Apr+is%3Aclosed")
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find(class_='btn-link selected').get_text()
  print(f"{e} pull requests closed 🟥") #blank space go brrr
'''
def if_starred(repo_link):
  """
  See if you stared a repo
  """
  page = requests.get(repo_link)
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find('div', class_='js-toggler-container js-social-container starring-container BtnGroup d-flex on')
  print(e)
  if e == None:
    print("You have not starred this repo yet. Why not star it? ;)")
  elif e :
    print("You have starred this repo. 🤩")
'''
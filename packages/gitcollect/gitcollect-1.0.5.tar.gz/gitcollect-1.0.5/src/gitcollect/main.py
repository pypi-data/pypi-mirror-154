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

def repo_languages(repo_link):
  """
  Gets the languages used in the repo
  """
  page = requests.get(repo_link)
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find_all(class_ = "d-inline-flex flex-items-center flex-nowrap Link--secondary no-underline text-small mr-3")[0].get_text()
  print(e)
  i=0
  try:
    while i < len(e):
      e = soup.find_all(class_ = "d-inline-flex flex-items-center flex-nowrap Link--secondary no-underline text-small mr-3")[i].get_text()
      print(e)
      i+=1
  except IndexError: #it works but why the error
    pass
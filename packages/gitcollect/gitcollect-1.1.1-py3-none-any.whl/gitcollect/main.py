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

def detect_license(repo_link):
  """
  Detects if the repo has a license
  """
  page = requests.get(repo_link)
  soup = BeautifulSoup(page.content, 'html.parser')
  try:
    e = soup.find(title = "LICENSE").get_text()
    print("This repo does have a license 📜")
  except: #it returns none
    print("This repo does not have a license")

def branches(repo_link):
  """
  Gets how many branches a repo has
  """
  page = requests.get(repo_link)
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find(class_ = "Link--primary no-underline").get_text()
  print(e)

def tags(repo_link):
  """
  Gets how many tags a repo has
  """
  page = requests.get(repo_link)
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find(class_ = "ml-3 Link--primary no-underline").get_text()
  print(e)

def last_commit(repo_link):
  """
  Gets the date and the commit number of the last commit to the repo

  If the date is today, that means the commit was made less than 24 hours ago
  """
  page = requests.get(repo_link)
  soup = BeautifulSoup(page.content, 'html.parser')
  e = soup.find(class_ = "d-flex flex-auto flex-justify-end ml-3 flex-items-baseline").get_text()
  print(e)
# def say_hello(name, age):
#   print(f"Hello {name} you are {age}years old")

# say_hello("nico", 12)
# say_hello(age = 12, name = "nico")

# list_of_numbers = [1,2,3]
# first = list_of_numbers[0]
# first = list_of_numbers[1]
# first = list_of_numbers[2]
# first, second, third = list_of_numbers
# print(first, second, third)

from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from selenium import webdriver

# wwr
# jobs = extract_wwr_jobs("python")
# print(jobs)

def extractor_indeed_jobs(keyword):
  pages = get_page_count(keyword)
  # print("Found", pages,"pages")
  browser_address = "./chromedriver_Win32/chromedirver.exe"
  browser = webdriver.Chrome(browser_address)
  results = []
  for page in range(pages):
    base_url = "https://kr.indeed.com/jobs"
    final_url =f"{base_url}?q={keyword}&start={page*10}"
    browser.get(final_url)
  
    soup = BeautifulSoup(browser.page_source, "html.parser")

    job_list = soup.find("ul", class_="jobsearch-ResultsList css-0")
    jobs = job_list.find_all('li', recursive = False) # recursive = 한번만 (재귀)
    # print(len(jobs))
    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone == None:
        # h2 = job.find("h2", class_="jobTitle")
        # a = h2.find("a")
        anchor = job.select_one("h2 a") # h2 에서 a를 가져와라 - dictionary로 가져온다!!!!!!!!!!!
        title = anchor['aria-label']
        link = anchor['href']
        company = job.find("span", class_ = "companyName")
        location = job.find("div", class_ = "companyLocation")    
        job_data = {
          'link' : f"https://kr.indeed.com/{link}",
          'company' : company.string.replace(",", " "),
          'location' : location.string.replace(",", " "),
          'position' : title.replace(",", " ")
        }
        results.append(job_data)
  return results
      # else:
      #   print("mosaic li")
    
def get_page_count(keyword):
  browser_address = "./chromedriver_Win32/chromedirver.exe"
  browser = webdriver.Chrome(browser_address)

  base_url = "https://kr.indeed.com/jobs?q="

  browser.get(f"{base_url}{keyword}")
  soup = BeautifulSoup(browser.page_source, 'html.parser')
  navigation = soup.find("nav", role ="navigation") # role -> role_ 말고 role로 입력!
  pages = navigation.find_all("div", recursive = False)
  count = len(pages)
  if count >= 5:
    return 5
  elif count == 0:
    return 1
  else:
    return count
    
# jobs = extractor_indeed_jobs("python")
# print(len(jobs))
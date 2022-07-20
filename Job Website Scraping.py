# import the necessary libraries for work
# note: The requests library allows fetch static HTML using python
# The beautifulsoup is used to parse the HTML page, to collect relevant information
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Declare your chosen website for scraping
URL = "https://realpython.github.io/fake-jobs/"

# Request for the html website content
page = requests.get(URL)

# Print the html content of the page
# print(page.text)

# Get the whole website content using beautiful soup and parse the html contents
soup = BeautifulSoup(page.content, "html.parser")

# Get all the job results from the div - results container class
results = soup.find(id="ResultsContainer")

# Get all the job elements from the div - card-content class
job_elements = results.find_all("div", class_="card-content")

# Loop through each of the job elements and extract the information you want(job title, company and location)
for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()
    # print(job_element, end="\n"*2)

# Let's find jobs with jobs containing the exact word "Python", filter for Python jobs
python_jobs = results.find_all("h2", string="Python")
print(python_jobs)

# Let's find jobs that contains the word "Python" using lambda function, making code flexible
python_jobs = results.find_all(
    "h2", string=lambda text: "python" in text.lower()
)

# Total python jobs in the list
print(len(python_jobs))

# List the python jobs available
for python_job in python_jobs:
    # title_element = job_element.find("h2", class_="title")
    print(python_job.text.strip())


# Getting the filtered python job with all necessary attributes from the great grand parents on the HTML codes
python_job_elements = [
    h2_element.parent.parent.parent for h2_element in python_jobs
]
print(python_job_elements)
Job_title = []
Company = []
Location = []
# Python Jobs without all the html tags and just the necessary information extracted along with the application link
for python_job_element in python_job_elements:
    title_element = python_job_element.find("h2", class_="title")
    company_element = python_job_element.find("h3", class_="company")
    location_element = python_job_element.find("p", class_="location")
    Job_title.append(title_element.text.strip())
    Company.append(company_element.text.strip())
    Location.append(location_element.text.strip())

    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()

    # Include links for just Python Job applications, used the position in array to solve it
    link_url = python_job_element.find_all("a")[1]["href"]
    print(f"Apply here: {link_url}\n")

    # Get all links associated with the python job listing including the applying links and learning more links
    # links = python_job_element.find_all("a")
    # for link in links:
    #     link_url = link["href"]
    #     print(f"Apply here: {link_url}\n")

df = pd.DataFrame({'Job Title':Job_title,'Company':Company,'Locations':Location})
df.to_csv('Jobwebsite.csv', index=False, encoding='utf-8')
import xlwt
import urllib
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

# Function find_jobs extracts information from our desired webistes alongside job_titles,location and another information
# this function extracts are stored in the joblist xls file
def find_jobs (website, job_title, location, desired_information, filename= "JobList.xls"):

     

    if website == 'jobberman':
        job_soup = load_jobberman_jobs(job_title, location)
        jobs_list,num_listings = extract_job_information_jobberman(job_soup,desired_information)


    # if website == 'myjobmag':
    #     location_of_driver = os.getcwd()
    #     driver = initiate_driver(location_of_driver,browser='chrome')
    #     job_soup = make_job_search(job_title,location,driver)
    #     jobs_list,num_listings = extract_job_information_myjobmag(job_soup,desired_information)

    save_jobs_to_excel(jobs_list,filename)

    print(f"{num_listings} new jobs retrieved from {website}. stored in {filename}")


#Generic Functions 
def save_jobs_to_excel(jobs_list,filename):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel(filename)



#function for Jobberman 
def load_jobberman_jobs(job_title,location):
    getVars = {'q': job_title,'l':location,'fromage':'last','sort': 'date'}
    url= ("https://www.jobberman.com/jobs/" + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content,"html.parser")
    job_soup = soup.find("div",class_ = "flex-mid-container max-width--1280 flex-direction-top-to-bottom--under-xl")
    return job_soup

def extract_job_information_jobberman(job_soup,desired_information):
    job_elems = job_soup.find_all('div',class_ = "search-result__header")

    cols = []
    extracted_info = []

    if 'titles' in desired_information:
        titles = []
        cols.append('titles')
        for job_elem in job_elems: 
            titles.append(extract_job_title_jobberman(job_elem))
        extracted_info.append(titles)
    
    if 'companies' in desired_information:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_jobberman(job_elem))
        extracted_info.append(companies)

    if 'links' in desired_information:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_jobberman(job_elem))
        extracted_info.append(links)


    if 'date_listed' in desired_information:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(extract_date_jobberman(job_elem))
        extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]]= extracted_info[j]
        
    num_listings = len(extracted_info[0])

    return jobs_list,num_listings

def extract_job_title_jobberman(job_elem):
    title_elem = job_elem.find('h3', _class = "search-result__job-title metrics-apply-now")
    title = title_elem.text.strip()
    return title

def extract_company_jobberman(job_elem):
    company_elem = job_elem.find('div', _class = "if-content-panel padding-lr-20 flex-direction-top-to-bottom--under-lg align--start--under-lg search-result__job-meta")
    company = company_elem.text.strip()
    return company 
    
def extract_link_jobberman(job_elem):
    link = job_elem.find('a')['href']
    link = 'www.jobberman.com/' + link
    return link


def extract_date_jobberman(job_elem):
    date_elem = job_elem.find('div', _class = "if-wrapper-column align-self--end text--right")
    date = date_elem.text.strip()
    return date













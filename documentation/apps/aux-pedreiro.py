from browser import browser

# Variables
jobTitle = 'auxiliar+de+pedreiro'
location = 'Brasil'
geoId = '106057199'

# Constants
url = f'https://www.linkedin.com/jobs/search?keywords={jobTitle}&location={location}&geoId={geoId}&trk=public_jobs_jobs-search-bar_search-submit'


# Script
driver = browser()
driver.get(url)
# Writing headers to a CSV file

headers = ['Job', 'Company', 'Location', 'Status', 'Published', 'URL', 'Today']
path_date = datetime.now().strftime("%Y-%m-%d")
file_path = f'C:/Users/Ana Carolina/OneDrive/Documents/_dev/_localpipeline/output/_scrapingjobs/linkedin_{path_date}.csv'

with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(headers)


# Writing registers to a CSV file

for i in range(0, jobs):

    # Splitting the text using '\n' as the delimiter
    items = re.split(r'\n', job_list[i])
    url = job_links[i]
    
    # Creating CSV register
    job_title = items[0]
    company_name = items[2]
    job_location = items[3]
    status = items[3]
    published = items[4]
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [job_title, company_name, job_location, status, published, url, today]

    # Writing registers to a CSV file
    with open(file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(row)
        

print(f"New CSV file '{file_path}' has been created.")
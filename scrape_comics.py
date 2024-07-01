import requests
from bs4 import BeautifulSoup
import os

def download_images(url, output_dir, i):
    response = requests.get(url)
    response.raise_for_status()  

    soup = BeautifulSoup(response.content, 'html.parser')

    center_tags = soup.find_all('center')

    if len(center_tags) < 3:
        raise ValueError("The webpage does not have at least three <center> tags")

    third_center = center_tags[2]

    img_tags = third_center.find_all('img')

    os.makedirs(output_dir, exist_ok=True)

    count = 0

    for img_tag in img_tags:
        img_url = img_tag['src']
        if not img_url.startswith('http'):
            img_url = url + img_url  
        img_response = requests.get(img_url)
        img_response.raise_for_status()  
        name = str(i)+'_'+str(count) + '.jpg'
        
        img_filename = os.path.join(output_dir, name)
        
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_response.content)
            print(f"Downloaded {img_filename}")
        count +=1

issues = [
    # 208, 210, 211, 212, 213, 214, 215, 216, 217, 218, 
    # 223, 224, 225, 226, 227, 229, 230, 
    231, 232, 233, 
    234, 235, 236, 238, 239, 240, 241, 242, 243, 244, 
    245, 246, 247, 248, 249, 250, 290, 291, 432, 500, 
    501, 502, 503, 504, 505, 506, 507, 508, 568, 569, 
    570, 571, 572, 573, 584, 585, 587, 588, 600, 692
]
output_dir = './downloaded_images/ExMachina'

# for issue in issues:
for issue in range(20,50):
    issue_no = '00'+str(issue) if issue <10 else '0'+str(issue)
    url = 'https://readallcomics.com/ex-machina-'+issue_no
    download_images(url, output_dir, issue)



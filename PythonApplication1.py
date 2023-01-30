from selenium import webdriver
import time
import os
import shutil

def rename_last_downloaded_file(dummy_dir, destination_dir, new_file_name):
    def get_last_downloaded_file_path(dummy_dir):
        """ Return the last modified -in this case last downloaded- file path.

            This function is going to loop as long as the directory is empty.
        """
        while not os.listdir(dummy_dir):
            time.sleep(1)
        return max([os.path.join(dummy_dir, f) for f in os.listdir(dummy_dir)], key=os.path.getctime)

    while '.part' in get_last_downloaded_file_path(dummy_dir):
        time.sleep(1)
    shutil.move(get_last_downloaded_file_path(dummy_dir), os.path.join(destination_dir, new_file_name))

# change to your own path
download_folder = "/Users/kudan/Documents/GitHub/ki-digital-corpus/Data"
dummy_folder = "/Users/kudan/Documents/GitHub/ki-digital-corpus/Dummy"

options = webdriver.FirefoxOptions()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", dummy_folder)
options.set_preference("browser.download.useDownloadDir", True)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
options.set_preference("pdfjs.disabled", True)

# change to your own path to the executable file
driver = webdriver.Firefox(executable_path='/Users/kudan/Documents/GitHub/ki-digital-corpus/geckodriver-v0.32.0-win64/geckodriver', options=options)
driver.maximize_window()
driver.get("http://www.korea-copy.com/rodong/?sess=4CGS2kzopS2MB8cTnhYaY082zT4YEvz2SdEGWr3qkGU%3D")
time.sleep(5)

entry_link = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[1]/table/tbody/tr[4]/td/a')
entry_link.click()
time.sleep(5)

driver.switch_to.window(driver.window_handles[1])
years = driver.find_elements_by_xpath('/html/body/div/div[4]/font/dl/a')


#years = driver.find_elements_by_xpath('//*[@id="main"]/font/dl/a')
for year in years[8:10]:
    year_name = year.text
    year_link = year.get_attribute('href')
    driver.execute_script("window.open('{}', 'secondtab')".format(year_link))
    time.sleep(3)
    driver.switch_to.window('secondtab')
    months = driver.find_elements_by_xpath('/html/body/div')
    i = 0
    for month in months:
        i = i + 1
        rows = month.find_elements_by_xpath('table/tbody/tr')
        for row in rows[2:]:
            tds = row.find_elements_by_xpath('td')
            for td in tds:
                day = td.find_elements_by_xpath('a')
                if len(day) != 0:
                    day_name = day[0].text
                    day[0].click()
                    time.sleep(15)
                
                    file_name = '{}_{}_{}'.format(year_name, i, day_name) + "." + 'pdf'
                    rename_last_downloaded_file(dummy_folder, download_folder, file_name)
    
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)

driver.close()
driver.switch_to.window(driver.window_handles[0])
driver.close()






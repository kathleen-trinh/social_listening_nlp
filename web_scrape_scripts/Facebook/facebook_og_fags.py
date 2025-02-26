#!/usr/bin/env python
# coding: utf-8

# In[1]:


#####################################################################################
# facebook_og_tags.py
#
# Script for using Facebook's Sharing Debugger for getting og tags,
# scraping the output from the application.
# Tools: Selenium, ChromeDriver
# Data Organizer: Pandas
#
# Version: 1
# Date Created: 03/05/2019
# Last Modified: 03/13/2019
#####################################################################################


# In[2]:


##### IMPORTING PACKAGES ############################################################
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import string
import time


# In[3]:


##### GLOBAL VARIABLES ##############################################################

# Path to where you have ChromeDriver installed (CHANGE AS NEEDED)
# Type: string
# Note: Please end it with "/chromedriver" (assuming "chromedriver" is the name of the file)
chromedriver = "/Users/kathleen.trinh/Documents/chromedriver"

# URL to Facebook login, which will redirect to Facebook's Sharing Debugger
# (UPDATE IF NEEDED, OTHERWISE DO NOT CHANGE)
# Type: string
FBSD_login = "https://www.facebook.com/login/?next=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fdebug%2F"

# URL to Facebook's Sharing Debugger
# (UPDATE IF NEEDED, OTHERWISE DO NOT CHANGE)
# Type: string
FBSD_URL = "https://developers.facebook.com/tools/debug/"

# Timeout for __ seconds (CHANGE AS NEEDED depending on strength of Internet connection)
# Type: integer
# Note: This is used in driver.set_page_load_timeout(timeout_for)
# where the page will timeout after timeout_for seconds.
timeout_for = 60

# Time to sleep for (CHANGE AS NEEDED depending on strength of Internet connection)
# Type: integer
# Note: This is used in function: time.sleep(time_to_sleep)
#       where the code will pause for time_to_sleep seconds, allowing page to load.
#       You may insert this function where needed if script does not run well as is.
time_to_sleep_for = 5

# Path to the main folder your project is in (CHANGE AS NEEDED)
# Type: string
main_folder = "C://Users/kathleen.trinh/Documents/Facebook_og_Tags/test/"

# Name of the folder containing the input .txt files
# Type: string ending with "/"
# Note: Please make sure this folder contains ONLY .txt files encoded in ANSI.
#       to be used as input and NO OTHER files or directories.
input_folder = "input/"
input_path = main_folder + input_folder

# Name of the folder you want to put the output files in
# Type: string ending with "/"
output_folder = "output/"
output_path = main_folder + output_folder

# File name you want to save the output .csv file as (CHANGE AS NEEDED)
# Type: string ending with ".csv"
file_name_timestamp = "190313"
domain_name = "test"
file_name_csv = file_name_timestamp + "_Facebook_og_Tags_" + domain_name + "_output.csv"

# File name you want to save the output .txt file as (CHANGE AS NEEDED)
# Type: string ending with ".txt"
file_name_txt = file_name_timestamp + "_Facebook_og_Tags_" + domain_name + "_output.txt"


# In[4]:


##### GLOBAL VARIABLES FOR COLUMNS IN OUTPUT (DO NOT CHANGE) ########################

Warnings_set = set()
When_and_How_fields = ["Time Scraped", "Response Code", "Fetched URL", "Redirect Path", "Server IP"]
OG_Properties_set = set()


# In[5]:


#####################################################################################
##### FUNCTIONS FOR SCRAPING ########################################################
#####################################################################################

##### GENERAL FUNCTIONS #############################################################

# NOTE: This function assumes that all files in the directory are .txt files
#       and does not perform any format checking to verify file type or content.
def get_filenames():
    """
    This function takes in no inputs
    and returns a list of strings (filenames),
    where each string is a filename found in the directory
    provided as a global variable (input_path).
    """
    print("Detecting input .txt files...")
    filenames = []
    counter = 0
    for filename in os.listdir(input_path):
        print("\t", filename)
        filenames.append(filename)
        counter += 1
    print("Number of input .txt files detected:", counter)
    return filenames

def open_URL(URL):
    """
    This function takes in a string (URL)
    and opens the given URL in the Chrome Driver window.
    """
    try:
        print("Attempting to open URL:", URL, "...")
        driver.set_page_load_timeout(timeout_for)
        driver.get(URL)
    except TimeoutException as ex:
        print("TimeoutException has been thrown. " + str(ex))

def input_URL(page_URL):
    """
    This function takes in a string (page_URL),
    which is a URL the user wants to put into FB's Sharing Debugger,
    opens the main Facebook Sharing Debugger page,
    finds the element on the page corresponding to the input text box,
    and inputs the given URL.
    """
    try:
        # Load default Facebook Sharing Debugger page if not currently on page
        # (e.g. on a URL's result page)
        if driver.current_url != FBSD_URL:
            open_URL(FBSD_URL)
        # Find the element for the URL input box
        input_element = driver.find_element_by_css_selector("#u_0_5")
        # Input the given page URL
        input_element.send_keys(page_URL)
        # Hit the ENTER key
        input_element.send_keys(Keys.ENTER)
    except:
        print("[ERROR] Unknown error trying to load Facebook's Sharing Debugger:", FBSD_URL)

# NOTE: This function is only called when the user is met with an error page
#       after inputting a URL into FB's Sharing Debugger.
def get_Error_Message():
    """
    This function takes in no inputs,
    finds the element on the page corresponding to the red box
    (which has the icon of an exclamation mark inside a triangle on the left),
    and returns a string (Error_Msg), which is the displayed error message text.
    """
    # Get the error message in the red box (preceded by the icon of the exclamation mark inside the triangle)
    print("Getting error message...")
    try:
        Error_Msg_element = driver.find_element_by_xpath("//div[@class='_585r _50f4']")
        Error_Msg = get_element_text(Error_Msg_element.find_element_by_xpath("//span[@class='_c24 _2iem']"))
        return Error_Msg
    except:
        print("\t[ERROR] Unknown error trying to get red error message on page.")

# NOTE: This function is only called when the user is met with a page
#       saying that the given URL has not been scraped recently.
def click_Fetch_new_info():
    """
    This function takes in no inputs.
    finds the element on the page corresponding to the 'Fetch new Information' button,
    and clicks it.
    """
    print("\tFinding 'Fetch new information' button and clicking upon detection...")
    try:
        btn = driver.find_element_by_css_selector("#u_0_8 > button")
        btn.click()
        time.sleep(1)
        print("\t\tClicked 'Fetch new information' button.")
        return 0
    except:
        print("\t\t[ERROR] Unknown error occurred trying to click 'Fetch new information' button.")
        return -1

# NOTE: This is a universal function for getting the default text associated with a web element.
def get_element_text(element):
    return element.text
    
# NOTE: This is a universal function (for results page) used to get text of the element:
#       <span class="_c24 _2iem"> [TEXT HERE] </span>
#       for each element in given list of web elements.
def get_span_texts(web_elements):
    """
    This function takes in a list of Selenium Web Elements (web_elements),
    assuming that each element has another element called ".//span[@class='_c24 _2iem']" inside of it,
    retrieves the text corresponding to the above mentioned span element,
    and returns a list of string (texts) in which each string is the text found in the span element
    of each of the given web elements.
    """
    texts = []
    for web_element in web_elements:
        element = web_element.find_element_by_xpath(".//span[@class='_c24 _2iem']")
        texts.append(element.text)
    return texts


# In[6]:


##### FUNCTIONS FOR WARNING SECTION #################################################
    
def check_for_Warnings():
    """
    This function takes in no inputs,
    attempts to find the section titled 'Warnings That Should Be Fixed',
    and returns a Boolean True or False based on whether the section is
    present on the page or not.
    """
    print("Checking for 'Warnings That Should Be Fixed' section...")
    try:
        warnings_section_element = driver.find_element_by_xpath("//div[@class = '_4-u2 _57mb _1u44 _5kz- _4-u8']")
        print("\t'Warnings That Should Be Fixed' section detected.")
        return True
    except NoSuchElementException:
        print("\tNo 'Warnings That Should Be Fixed' section detected.")
        return False
    except:
        print("\t[ERROR] Unknown error occurred trying to check for 'Warnings That Should Be Fixed' section.")
        return -1

# NOTE: The following 3 functions are only called if a Warnings section is detected.

def click_Show_All_Warnings():
    """
    This function takes in no inputs,
    attempts to find the 'Show All Warnings' button on the page,
    and clicks it if found.
    Note that this button is only present if there is more than 1 warning.
    """
    # Find and click the element for the "Show All Warnings" button
    print("Finding 'Show All Warnings' button and clicking upon detection...")
    try:
        # Sometimes css selector is "#u_3_1 > li.showAll > div"
        #btn = driver.find_element_by_css_selector("#u_0_1 > li.showAll > div > span")
        btn = driver.find_element_by_xpath("//div[@class = '_4sj8 _2pi0 _52jv']")
        btn.click()
        time.sleep(1)
        print("\tClicked 'Show All Warnings' button.")
        return 0
    except NoSuchElementException:
        print("\tNo 'Show All Warnings' button detected.")
        return 1
    except:
        print("\t[ERROR] Unknown error occurred trying to click 'Show All Warnings' button.")
        return -1
    
def get_Warning_Types():
    """
    This function takes in no inputs,
    finds the elements on the page corresponding to the titles of the warnings,
    retrieves the text of the titles,
    and returns a list of string in which each string is the title of a warning.
    """
    warning_type_elements = driver.find_elements_by_xpath("//div[@class='_4si_ _2pi0 lfloat _ohe']")
    warning_types = get_span_texts(warning_type_elements)
    return warning_types

def get_Warning_Descriptions():
    """
    This function takes in no inputs,
    finds the elements on the page corresponding to the descriptions of the warnings,
    retrieves the text of the descriptions,
    and returns a list of string in which each string is a description of a warning.
    """
    warning_desc_elements = driver.find_elements_by_xpath("//div[@class='_2pi0 _42ef']")
    warning_descs = get_span_texts(warning_desc_elements)
    return warning_descs

def get_Warnings():
    """
    This function takes in no inputs and checks if there is a Warnings section.
    If there is, it will get the Warning Type and Warning Description of each warning,
    put the information into a dictionary, and return the dictionary (Warnings_dict)
    in which each key is a Warning Type and each corresponding value is a Warning Description.
    Else, it will return an empty dictionary.
    """
    Warnings_dict = {}
    if check_for_Warnings() == True:
        click_Show_All_Warnings()
        warning_types = get_Warning_Types()
        #print("\tWarning Types:", warning_types)
        warning_descs = get_Warning_Descriptions()
        #print("\tWarning Descriptions:", warning_descs)
        if len(warning_types) != len(warning_descs):
            print("\t\tLength of warning types does not equal length of warning descriptions.")
            return -1
        #return list(zip(warning_types, warning_descs))
        for i in range(0, len(warning_types)):
            Warnings_dict[warning_types[i]] = warning_descs[i]
            Warnings_set.add(warning_types[i])
    return Warnings_dict


# In[7]:


##### FUNCTIONS FOR THE 3 TABLES ####################################################

# NOTE: For each URL that is analyzed by the Facebook Sharing Debugger,
#       there will always be the following 3 sections / tables:
#       1. "When and how we scraped the URL" - composed of max 7(?) rows
#       2. "Based on the raw tags, we constructed the following Open Graph properties" - composed of max 12(?) rows
#       3. "URLs" - composed of 4 rows (URLs to other FB tools)

def get_table_elements():
    """
    This function takes in no inputs,
    finds the table elements on the page corresponding to the 3 section,
    and returns a list of Selenium Web Elements (table_elements)
    in which each element is a table element for a section.
    """
    print("Getting the 3 table elements...")
    table_elements = driver.find_elements_by_xpath("//table[@class='_4-ss _50-p']")
    if len(table_elements) != 3:
        print("\t[WARNING] Detected", len(table_elements), "table elements on page. Should be 3.")
    return table_elements

def get_table_content_elements(table_element):
    """
    This function takes in a Selenium Web Element (table_element),
    which should be a table element corresponding to a section (found from the above function),
    gets the Information Type as a string and the element corresponding to
    the Information Description of each listed item in the table,
    and returns a list of 2-item tuples such that:
    [(string representing the Information Type, Selenium Web Element corresponding to field's value), ...]
    """
    print("\tGetting table's contents...")
    info_type_elements = table_element.find_elements_by_xpath(".//td[@class='_2wq5']")
    info_types = get_span_texts(info_type_elements)
    info_desc_elements = table_element.find_elements_by_xpath(".//td[@class='_2wq4']")
    print("\t\tDetected", len(info_type_elements), "info types &", len(info_desc_elements), "info descriptions.")
    if len(info_types) != len(info_desc_elements):
        print("\t\t[ERROR]Length of info types does not equal length of info descriptions.")
        return -1
    elif len(info_type_elements) == 0:
        print("\t\t[ERROR]Did not detect any elements for info types.")
        return -2
    elif len(info_desc_elements) == 0:
        print("\t\t[ERROR]Did not detect any elements for info descriptions.")
        return -3
    return list(zip(info_types, info_desc_elements))


# In[8]:


##### FUNCTIONS FOR WHEN AND HOW SECTION ############################################
# The "When and how we last scraped the URL" section is the 1st table on the page
# under the Warnings section (if there is one)
# and is composed of at most(?) 7 rows:
# 1. Time Scraped
# 2. Response Code
# 3. Fetched URL
# 4. Canonical URL - NOT CAPTURED IN THIS SCRIPT
# 5. Redirect Path
# 6. Link Preview - NOT CAPTURED IN THIS SCRIPT
# 7. Server IP

def get_Time_Scraped(element):
    """
    This function takes in a Selenium Web Element (element)
    corresponding to the Information Description part of the "Time Scraped" field,
    and returns a tuple of strings where the first item is the timestamp
    and the second item is the UNIX timestamp.
    Note: The final output does not include the UNIX timestamp, but it is still extractable from here.
    """
    info_element = element.find_element_by_xpath(".//abbr")
    timestamp = info_element.get_attribute("title")
    utime = info_element.get_attribute("data-utime")
    #display_text = info_element.text #Example: "2 hours ago"
    return (timestamp, utime)

def get_Redirect_Path(element):
    """
    This function takes in a Selenium Web Element (element)
    corresponding to the Information Description part of the "Redirect Path" field,
    gets the title and values of each of the items in the field,
    and returns a list of 2-item tuples such that:
    [(string of a Redirect Path title, string of the corresponding value), ...]
    """
    RP_info = []
    tr_elements = element.find_elements_by_xpath(".//tr")
    for tr_element in tr_elements:
        RP_title = tr_element.find_element_by_xpath(".//td[1]").text
        RP_value = tr_element.find_element_by_xpath(".//td[3]").text
        RP_info.append((RP_title, RP_value))
    return RP_info

def get_When_and_How(table_element):
    """
    This function takes in a Selenium Web Element (table_element),
    which should be the table element corresponding to the Why and How section,
    gets the titles and values of each field / row,
    and returns a dictionary containing the extracted information in which
    each key is a title of a field and each value is the corresponding value of the field.
    """
    WhenAndHow_dict = {}
    table_content_elements = get_table_content_elements(table_element)
    for i in range(0, len(table_content_elements)):
        if table_content_elements[i][0] == "Time Scraped":
            WhenAndHow_dict["Time Scraped"] = get_Time_Scraped(table_content_elements[0][1])
        elif table_content_elements[i][0] == "Canonical URL":
            pass
        elif table_content_elements[i][0] == "Redirect Path":
            WhenAndHow_dict["Redirect Path"] = get_Redirect_Path(table_content_elements[4][1])
        elif table_content_elements[i][0] == "Link Preview":
            pass
        else:
            WhenAndHow_dict[table_content_elements[i][0]] = get_element_text(table_content_elements[i][1])
    return WhenAndHow_dict


# In[9]:


##### FUNCTIONS FOR RAW TAGS SECTION ################################################
# The "Based on the raw tags, we constructed the following Open Graph properties" section
# is the 2nd table on the page and is composed of at most(?) 12 rows in any order(?):
#  1. og:url
#  2. og:type
#  3. og:title
#  4. og:updated_time
#  5. og:description
#  6. og:site_name
#  7. og:image
#  8. ia:markup_url
#  9. ia:markup_url_dev
# 10. ia:rules_url
# 11. ia:rules_url_dev
# 12. og:image:alt
# [*] A button that reads: "Show All Raw Tags", which opens another section if clicked on.

def get_OG_Properties(table_element):
    """
    This function takes in a Selenium Web Element (table_element),
    which should be the element corresponding to the Open Graph Properties section,
    gets the titles and values of each field / row,
    and returns a dictionary containing the extracted information in which
    each key is a type of Open Graph Property and each value is the corresponding value of that property.
    """
    OG_Properties_dict = {}
    table_content_elements = get_table_content_elements(table_element)
    for i in range(0, len(table_content_elements)):
        OG_Properties_dict[table_content_elements[i][0]] = get_element_text(table_content_elements[i][1])
        OG_Properties_set.add(table_content_elements[i][0])
    return OG_Properties_dict


# In[10]:


##### FUNCTIONS TO WRAP IT UP #######################################################

def get_OG_Tag_Report(URL):
    """
    This function takes in a string (URL),
    inputs the URL into FB's Sharing Debugger,
    extracts information from the displayed results page, if successful,
    and returns a list of 4 dictionaries where:
    1. The 1st dictionary "URLandError" contains 2 keys: "URL" and "Error" where
       "URL" is the inputted URL and
       "Error" is "Malformed URL", "Invalid URL", "Unknown Error", or "No Error"
       depending on whether there was an error or not when getting the results page.
    2. The 2nd dictionary "Warnings" contains information from the Warnings section
       returned from the "get_Warnings()" function. Note that if there are no warnings
       for the given URL, it is an empty dictionary.
    3. The 3rd dictionary "WhenAndHow" contains information from the When and How section
       returned from the "get_When_and_How(table_element)" function.
    4. The 4th dictionary "OG_Properties" contains information from the Open Graph Properties section
       returned from the "get_OG_Properties(table_element)" function.
    """
    print("Getting OG Tag Report for URL:", URL, "...")
    # Load Facebook Sharing Debugger page and input a URL
    input_URL(URL)
    # Note the input URL
    URLandError = {"URL": URL}
    # Get the 3 default table elements on the page
    table_elements = get_table_elements()
    if len(table_elements) == 0:
        Error_Msg = get_Error_Message()
        if Error_Msg == "Could not scrape URL because it was malformed.":
            print("[ERROR] Input URL:", URL, "is malformed. Unable to get OG Tag Report.")
            URLandError["Error"] = "Malformed URL"
            return [URLandError]
        elif Error_Msg == "Your input was not a valid URL.":
            print("[ERROR] Input URL:", URL, "is an invalid URL. Unable to get OG Tag Report.")
            URLandError["Error"] = "Invalid URL"
            return [URLandError]
        elif Error_Msg == "This URL hasn't been shared on Facebook before.Fetch new information":
            print("URL has not been shared on Facebook before. Will fetch new information for URL:", URL)
            click_Fetch_new_info()
            cycle_count = 12
            while (len(get_table_elements()) == 0 and cycle_count != 0):
                print("\t\tWaiting for page to load... Wait cycle remaining =", cycle_count)
                time.sleep(time_to_sleep_for)
                cycle_count -= 1
            table_elements = get_table_elements()
            if len(table_elements) == 0:
                print("\t\t[ERROR] Unable to detect table elements on page. Unable to get OG Tag Report for URL:", URL)
                URLandError["Error"] = "Unknown ERROR"
                return [URLandError]
    # Get the Warnings
    Warnings = get_Warnings()
    print(len(Warnings), "warnings detected.")
    for key, val in Warnings.items():
        print("\t[Warnings That Should Be Fixed]", key, "=", val)
    # Get the When and How
    WhenAndHow = get_When_and_How(table_elements[0])
    print(len(WhenAndHow), "fields captured from 'When and how we last scraped the URL'.")
    for key, val in WhenAndHow.items():
        print("\t[When and how we last scraped the URL]", key, "=", val)
    # Get the Open Graph Properties
    OG_Properties = get_OG_Properties(table_elements[1])
    print(len(OG_Properties), "fields captured from 'Based on the raw tags, we constructed the following Open Graph properties'.")
    for key, val in OG_Properties.items():
        print("\t[Open Graph Properties]", key, "=", val)
    # Note that results actually loaded for input URL
    URLandError["Error"] = "No Error"
    # Return list of dict for each section
    return [URLandError, Warnings, WhenAndHow, OG_Properties]

def get_Reports(filename):
    """
    This function takes in a string (filename),
    which should be a .txt file containing 1 URL per line
    to input into the Facebook Sharing Debugger,
    opens the file and reads it,
    getting the report for each file,
    and returns a list of lists in which each inner list
    contains 4 dictionaries with the extracted information for 1 URL.
    """
    print("\nGetting OG Tag Reports for URLs in filename:", filename, "...\n")
    reports = []
    with open(input_path + filename) as f:
        URLs = f.readlines()
        URLs = [x.strip() for x in URLs]
    for URL in URLs:
        OG_Tag_Report = get_OG_Tag_Report(URL)
        reports.append(OG_Tag_Report)
    return reports # list of lists of 4 dicts

def get_ALL_Reports(filenames):
    """
    This function takes in a list of strings (filenames)
    where each filename should be a .txt file of URLs.
    For each file, it will get the information for each URL in the file
    and append it to the list "reports_per_file".
    Then for each report for an individual URL, it will construct a dictionary (individual_report)
    in which each key is the title of a field on the page, regardless of which section it is in
    and each value is the corresponding value of that field.
    Each newly constructed dictionary representative of an individual URL is then appended to
    the list "ALL_Reports", which is a list of dictionaries in which each dictionary holds the
    information of a single URL, regardless of which input .txt file it was listed on.
    This function returns this list of dictionaries (ALL_Reports).
    """
    ALL_Reports = []
    reports_per_file = []
    for filename in filenames:
        reports_per_file.append(get_Reports(filename))
    print("len(reports_per_file) =", len(reports_per_file))
    for reports_per_URL in reports_per_file:
        print("len(reports_per_URL) =", len(reports_per_URL))
        for individual_report in reports_per_URL:
            print("\n", individual_report, "\n")
            report = dict()
            if len(individual_report) == 4:
                # Unravel URL and Error:
                for key, val in individual_report[0].items():
                    report[key] = val
                # Unravel Warnings
                for key, val in individual_report[1].items():
                    report[key] = val
                # Unravel When and How
                for key, val in individual_report[2].items():
                    if key == "Time Scraped":
                        report[key] = val[0]
                    elif key == "Redirect Path":
                        RP_str = ""
                        for item in val: # for item (tuple) in val (list of tuples)
                            RP_str = RP_str + item[0] + ": " + item[1] + "\n"
                        report[key] = RP_str
                    else:
                        report[key] = val
                # Unravel OG Properties
                for key, val in individual_report[3].items():
                    report[key] = val
            else:
                # Unravel URL and Error:
                for key, val in individual_report[0].items():
                    report[key] = val
            ALL_Reports.append(report)
    return ALL_Reports # list of dicts


# In[11]:


##### IMPLEMENTATION ################################################################

### Set up Chrome Driver ###
print("Setting up ChromeDriver...")
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

### Open Facebook Sharing Debugger Login ###
open_URL(FBSD_login)
print("Please manually input login credentials.")


# In[36]:


### Get input filenames ###
filenames = get_filenames()


# In[37]:


### Use FB Sharing Debugger ###
data = get_ALL_Reports(filenames)


# In[38]:


### Make Pandas DataFrame ###
df = pd.DataFrame(data)


# In[39]:


# Display the constructed DataFrame
df


# In[41]:


# Print the constructed DataFrame to the terminal
print(df)


# In[43]:


# Export Pandas DataFrame object to a .csv file
df.to_csv((output_path + file_name_csv), index = None, header=True)


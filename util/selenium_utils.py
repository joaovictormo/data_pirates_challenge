from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def _init_browser(url):
    '''
    Utility function to open browser and access given URL

    Args:
        url (str): website's URL
    Returns:
        browser (obj): Selenium's webdriver object
    '''

    browser = webdriver.Firefox(executable_path="geckodriver.exe")
    browser.get(url)

    return browser


def _init_new_UF(strikes, browser):
    '''
    Utility function to select the desired UF

    Args:
        strikes (str): key strikes to reach the desired UF in the <select>
        browser (obj): Selenium's webdriver object
    '''

    # Finds the element with name="UF"
    elem = browser.find_element(By.NAME, 'UF')
    elem.click()
    # emulates strikes on keys, to reach the desired <option> on the <select>
    elem.send_keys(strikes)
    # strikes 'Enter' to select the chosen option
    elem.send_keys(Keys.RETURN)


def iterate_table_rows(browser, is_first_page, last_id):
    '''
    Utility function to iterate through table rows

    Args:
        browser (obj): Selenium's webdriver object
        is_first_page (boolean): indicates whether the current page is the first for the current UF
        last_id (int): the last id in the final dictionary
    Returns:
        result (dict): resulting dictionary with all table rows from the current page
    '''

    table_xpath = "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table"

    if is_first_page:
        table_xpath += "[2]"

    table = browser.find_element_by_xpath(table_xpath)
    rows = table.find_elements(By.TAG_NAME, "tr")
    result = []
    for row in rows[2:]:
        location = row.find_elements(By.TAG_NAME, "td")[0]
        str_cep_range = row.find_elements(By.TAG_NAME, "td")[1].text
        cep_range = str_cep_range.replace(' ', '').split('a')

        if last_id == 0:
            last_id = 1
            result.append({'id': last_id,
                           'location': location.text,
                           'cep_range': cep_range})
        else:
            last_id += 1
            result.append({'id': last_id,
                           'location': location.text,
                           'cep_range': cep_range})

    return result


def iterate_uf_pages(url, list_strikes, next_page_xpath):
    '''
    Utility function to iterate through UF and pages

    Args:
        url (str): website's URL
        list_strikes (list): list of key strikes to reach the desired UF in the <select>
        next_page_xpath (str): the XPath of the anchor tag to navigate to the next page
    Returns:
        tab_rows (dict): resulting dictionary with all table rows from the current page
    '''

    for idx, strikes in enumerate(list_strikes):
        print(f"Iniciada a obtenção dos dados do strike: {strikes}")
        browser = _init_browser(url)  # fetches the object browser

        _init_new_UF(strikes, browser)  # selects an UF

        btn_search = browser.find_element_by_xpath(
            "//input[@value='Buscar']")  # finds the button 'Buscar'

        btn_search.click()  # clicks button 'Buscar'

        if idx == 0:
            # first iteration through table rows, must create the resulting dictionary
            tab_rows = iterate_table_rows(
                browser=browser, is_first_page=True, last_id=0)
        else:
            # saves the id of the last iterated row from the last UF checked
            last_id = tab_rows[-1].get('id')
            # iterates through the rows of the first page of a new UF and increments the resulting dictionary
            tab_rows += iterate_table_rows(
                browser=browser,
                is_first_page=True,
                last_id=last_id)

        # checks if there's a next page link, navigates to it, and iterates through its rows, incrementing the resulting dictionary
        next_page = True
        while next_page:
            try:
                browser.find_element_by_xpath(next_page_xpath).click()
                last_id = tab_rows[-1].get('id')
                tab_rows += iterate_table_rows(
                    browser=browser,
                    is_first_page=False,
                    last_id=last_id)
            except:
                next_page = False

        browser.quit()
        print(f"Finalizada a obtenção dos dados do strike: {strikes}")

    return tab_rows

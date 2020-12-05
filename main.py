from util.selenium_utils import iterate_uf_pages


def uf_selector(list_uf):
    '''
    Utility function to generate the key strikes list, based on the uf's list.

    Args:
        list_uf (list): list of UFs
    Returns:
        list_strikes (list): list of key strikes to reach the desired UF in the <select>
    '''

    list_strikes = []

    for idx, uf in enumerate(list_uf):
        if idx == 0:
            # if it's the first UF of the list, appends its first letter to the strikes list
            list_strikes.append(uf[0])
        else:
            # checks if the first letter of the current UF equals the first letter of the last list_strikes item
            if uf[0] == list_strikes[idx - 1][0]:
                # if so, concatenates this first letter with the last list_strikes item into a new item
                list_strikes.append(list_strikes[idx - 1] + uf[0])
            else:
                list_strikes.append(uf[0])

    return list_strikes


def write_json(file_name, result_dict):
    '''
    Utility function to write the final json file.

    Args:
        file_name (str): the name of the file in which the results should be written
        result_dict (dict): the resulting dictionary from the scraping
    '''
    if not file_name.endswith('.json'):
        file_name += '.json'

    with open(file_name, 'w') as f:
        json.dump(result_dict, f)


if __name__ == "__main__":
    url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm'
    file_name = 'result.json'
    list_uf = ['ac', 'al', 'am', 'ap', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mg', 'ms', 'mt', 'pa', 'pb', 'pe', 'pi', 'pr', 'rj', 'rn', 'ro', 'rr', 'rs', 'sc', 'se', 'sp', 'to']
    next_page_xpath = "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[5]/a"

    list_strikes = uf_selector(list_uf)

    results = iterate_uf_pages(url, list_strikes, next_page_xpath)

    write_json(file_name, result_dict=results)

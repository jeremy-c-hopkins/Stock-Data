import requests
from lxml import html

mapping =  {
    "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/optvar.html": "optvar.xls",
    "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/vebitda.html": "vebitda.xls",
    "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/psdata.html": "psdata.xls",
    "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/pbvdata.html": "pbvdata.xls",
    "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/pedata.html": "pedata.xls"
}   

def get_industry_data():
    """
    Utilizes NYU website for getting industry wide data

    :return:
    :rtype:
    """
    links = mapping.keys()

    for link in links:
        url = requests.get(link, verify=False)

        info = html.fromstring(url.content)

        download = info.xpath("/html/body/div/div[1]/p[3]/a/text()")[0]

        response = requests.get(download, verify=False)

        with open(f"/home/bread/Coding/Finance/src/data/industries/{mapping[link]}", "wb") as file:
            file.write(response.content)

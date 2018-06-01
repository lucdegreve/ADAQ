# This code :
#   -connects to the greenfeed website, download the summary data
#   -save a csv file with the interesting data.
# Authors : Luc Degreve, Alexandre Mertens

from robobrowser import RoboBrowser    # website browsing
import xlrd                            # Excel file reading
from xlwt import Workbook              # Excel file writing

downloadData = True
convertToCsv = True


def getGFSummary(outFile):

    base_url = "https://greenfeed.c-lockinc.com/GreenFeed/home.php"
    base_url_xls = "https://greenfeed.c-lockinc.com/GreenFeed/downloaddata/downloaddailyfiles.php?file=GreenFeed_Summarized_Data_Belgium_90_91.xlsm"

    # definition of the browser
    browser = RoboBrowser()

    # Access the GreenFeed websiteand fill the login form
    browser.open(base_url)
    form = browser.get_form(action="checklogon.php")
    form["username"] = ''  # to be completed!
    form["password"] = ''  # to be completed!
    browser.session.headers['Referer'] = base_url
    browser.submit_form(form, submit='Login')

    # create the request to access the xls file
    request = browser.session.get(base_url_xls, stream=True)

    with open(outFile, "wb") as test:
        test.write(request.content)

    return()


def excelToCsv(xls_file):

    # xls file opening and sheet selection
    document = xlrd.open_workbook(xls_file)
    data = document.sheet_by_index(0)

    # Getting the number of lines and columns
    nbrow = data.nrows
    nbcol = data.ncols

    # Creation of the new file
    book = Workbook()
    sheet1 = book.add_sheet('view_data')

    for k in range(0, nbcol):
        for i in range(0, nbrow-1):
            sheet1.write(i, k, data.cell_value(rowx=(i+1), colx=k))

    return(book)


# get GF summary, transform to csv and save in the csv
xls_file = "../csv/GreenFeed/GF_Summary.xls"
if downloadData:
    getGFSummary(xls_file)

if convertToCsv:
    csv_file = excelToCsv(xls_file)
    csv_file.save("../csv/GreenFeed/GF_Summary.csv")

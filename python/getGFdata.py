from robobrowser import RoboBrowser

base_url = "https://greenfeed.c-lockinc.com/GreenFeed/home.php"
base_url_xls = "https://greenfeed.c-lockinc.com/GreenFeed/downloaddata/downloaddailyfiles.php?file=GreenFeed_Summarized_Data_Belgium_90_91.xlsm"

# definition of the browser
browser = RoboBrowser()

# Access the GreenFeed websiteand fill the login form
browser.open(base_url)
form = browser.get_form(action="checklogon.php")
form["username"] = ''
form["password"] = ''
browser.session.headers['Referer'] = base_url
browser.submit_form(form, submit='Login')

request = browser.session.get(base_url_xls, stream=True)

with open("test.xls", "wb") as xls_file:
    xls_file.write(request.content)


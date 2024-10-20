from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json

app = Flask(__name__)

# كوكيز Netflix
netflix_cookies = [
    {
        "domain": ".netflix.com",
        "expirationDate": 1736543851.843242,
        "hostOnly": False,
        "httpOnly": False,
        "name": "netflix-sans-normal-3-loaded",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "true"
    },
    {
        "domain": ".netflix.com",
        "expirationDate": 1760303860.558578,
        "hostOnly": False,
        "httpOnly": True,
        "name": "SecureNetflixId",
        "path": "/",
        "sameSite": "strict",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "v%3D3%26mac%3DAQEAEQABABSnwyyDJVcGzKSYB7zk4xBMTyG4ovvKLXI.%26dt%3D1728767860619"
    },
    {
        "domain": ".netflix.com",
        "expirationDate": 1728768131,
        "hostOnly": False,
        "httpOnly": False,
        "name": "firstLolomoAfterOnRamp",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "true"
    },
    {
        "domain": ".netflix.com",
        "expirationDate": 1728769660.488167,
        "hostOnly": False,
        "httpOnly": False,
        "name": "profilesNewSession",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "0"
    },
    {
        "domain": ".netflix.com",
        "expirationDate": 1760303860.558745,
        "hostOnly": False,
        "httpOnly": True,
        "name": "NetflixId",
        "path": "/",
        "sameSite": "lax",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "v%3D3%26ct%3DBgjHlOvcAxL4AkTIW-_O7bKFlm56YEtbOOh-u_1vByyS8weumQgRLrlMPeKjm7IRvbWZcOQldSBbx6_b_SjZmxFlwDvbd1ZAOmcIhKdZYoejxKW6iqZC2NeanS6vfzJ2xQ7rj1yCeCC8KrOejolahrU9PbJppygZ83OEgJr4HDE5ksjML-ZCKZ-TqKdrnayKE9s0fgZ6yRs75D8Z17mv_rNsmRoP0Fay4zKQek_3SnEck1RuJ8ewtP42CEuvd8rQjosWGve8687hyaQRTWt0DdorgDNUw78ttvcyz6t7Xs61dmScBAQKBjs9nn-WtLv84a503l7yqYKU2DD5_Cuvi7_0EFYvOddoVeuBhqY0dHb-o9bakz19xmjogMaZflOOGO2rJoKI0heU_NQYRt2WcqQl30odMb_YyD7VIqiU2cjt3mxA45LlrK20iXOXoAcp7qKQ7E-KGDnJvBdk9FPMR5vugYETTKzF3oCoBdoMkBQy3Z-1r569q56S1JH1RnTj7qAYBiIOCgwh34xKGhdLjUZtVTU.%26ch%3DAQEAEAABABTu521VvDhzebQc0TyBkteAMwfnzS-x13I."
    },
    {
        "domain": ".netflix.com",
        "expirationDate": 1760303852,
        "hostOnly": False,
        "httpOnly": False,
        "name": "OptanonConsent",
        "path": "/",
        "sameSite": "lax",
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "isGpcEnabled=0&datestamp=Sat+Oct+12+2024+22%3A17%3A32+GMT%2B0100+(GMT%2B01%3A00)&version=202407.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=2ebfea43-ab90-4f00-87d9-502f8ad4887b&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false"
    },
    {
        "domain": ".netflix.com",
        "expirationDate": 1728778647.137087,
        "hostOnly": False,
        "httpOnly": False,
        "name": "flwssn",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "71e5825b-31d0-4a2a-9f58-8e9b46590bbe"
    },
    {
        "domain": ".netflix.com",
        "expirationDate": 1736543851.843382,
        "hostOnly": False,
        "httpOnly": False,
        "name": "netflix-sans-bold-3-loaded",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "true"
    },
    {
        "domain": ".netflix.com",
        "expirationDate": 1760303728.437249,
        "hostOnly": False,
        "httpOnly": False,
        "name": "nfvdid",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "BQFmAAEBEEe9_KmgOkquKoPNfWyUfW9g_gZM0y6ff-36HCAKFlxTzcyH3Sp-XMbFBLNwVQaymn5789zfinoFtCfXqw2XMRttFy4Ji20iNLmXTQmKIXsPN0_MjFDzHZMdBFnp6zOPfonqwY3xyZ8V60BZwO_CsHL3"
    },
    {
        "domain": ".netflix.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "sawContext",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": True,
        "storeId": None,
        "value": "true"
    }
]

# إعداد Selenium
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # فتح المتصفح بالحجم الكامل
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# فتح موقع Netflix
driver.get("https://www.netflix.com")

# إضافة الكوكيز واحدة تلو الأخرى
for cookie in netflix_cookies:
    # إعداد الكوكيز وتنظيف البيانات
    cleaned_cookie = {
        'name': cookie['name'],
        'value': cookie['value'],
        'domain': cookie['domain'],
        'path': cookie.get('path', '/'),
        'secure': cookie.get('secure', False),
        'httpOnly': cookie.get('httpOnly', False),
    }
    
    # إضافة 'expiry' إذا كانت موجودة
    if 'expirationDate' in cookie:
        cleaned_cookie['expiry'] = int(cookie['expirationDate'])

    # إضافة الكوكي إلى المتصفح
    driver.add_cookie(cleaned_cookie)

# إعادة تحميل الصفحة لتفعيل الكوكيز
driver.get("https://www.netflix.com")

# إبقاء المتصفح مفتوحًا حتى إدخال أمر يدوي
input("اضغط على Enter لإغلاق المتصفح...")

# إغلاق المتصفح
driver.quit()


from get_brands import run_script
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
This script automates product scraping and interacts with a website using Selenium WebDriver. 

Features:
- Checks the language of the provided URL and converts it to English if it's in Arabic.
- Navigates to the website, handles cookies and pop-ups, and extracts brand names from product details.
- Performs a search based on the extracted brand name and navigates between pages.
- Includes functionality to call an external script for further processing.

البرنامج يقوم بعملية سحب بيانات المنتجات والتفاعل مع الموقع باستخدام Selenium WebDriver.

الخصائص:
- التحقق من لغة الرابط المدخل وتحويله إلى اللغة الإنجليزية إذا كان بالعربية.
- التنقل في الموقع، والتعامل مع ملفات تعريف الارتباط والنوافذ المنبثقة، واستخراج أسماء العلامات التجارية من تفاصيل المنتج.
- إجراء بحث باستخدام اسم العلامة التجارية المُستخرج والتنقل بين الصفحات.
- يتضمن وظيفة لاستدعاء سكربت خارجي لمعالجة إضافية.
"""

# BeautifulSoup and requests for potential further data processing
# مكتبة BeautifulSoup و requests لمعالجة البيانات في المستقبل
from bs4 import BeautifulSoup
import requests

# Prompt user for URL
# طلب الرابط من المستخدم
url_input = input("URL: ")

# =================== Check if the URL is in Arabic and convert to English if needed ===================================
# التحقق مما إذا كان الرابط باللغة العربية وتحويله إلى الإنجليزية إذا لزم الأمر


new_url = None
check_url_lang = url_input.split("/")
if "ar" in check_url_lang:
    removing_ar = url_input.split("ar")
    after_lang_url = removing_ar[-1]
    removing_ar[1] = "en"
    new_url = f"{removing_ar[0]}{removing_ar[-1]}{after_lang_url}"

print(f"\nNew URL With English Page: {new_url}")
# طباعة الرابط الجديد باللغة الإنجليزية



# ================================== Configure Chrome WebDriver options ===============================================
# إعداد خيارات WebDriver للـ Chrome


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(chrome_options)



# ==================================== Open the URL (new or original) =================================================
# فتح الرابط (الجديد أو الأصلي)
if new_url is None:
    driver.get(url_input)
else:
    driver.get(new_url)


#======================================  Initialize WebDriverWait with a timeout =======================================
# تهيئة WebDriverWait مع تحديد الوقت المحدد
wait = WebDriverWait(driver, 20)



# ======================== Wait for the cookie notice to be clickable and accept it ====================================
# انتظار قابلية النقر على إشعار الكوكيز والموافقة عليه
try:
    accept = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"cookieNotice\"]/div/div[2]/div[2]/button")))
    accept.click()
except Exception as e:
    driver.refresh()



# ==================== Wait for the delivery location popup to appear and close it =====================================
# الانتظار لظهور نافذة اختيار مكان التوصيل وإغلاقها
close_delivery_window = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/ngb-modal-window/div/div/app-location-selection-popup/div/div[1]/div[2]/i"))
)
print('تمت الموافقة')
close_delivery_window.click()



# ========================================== Wait for product details to load ==========================================
# انتظار تحميل تفاصيل المنتج
brand_name = None
try:

    product_details = wait.until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[1]/app-product-detail-page/section/div[3]/div/app-product-classifications/section"))
    )

    # Extract product details
    # استخراج تفاصيل المنتج
    box_details = product_details.text

    # Extract brand name from details
    # استخراج اسم العلامة التجارية من التفاصيل
    for line in box_details.split("\n"):
        if "Brand" in line:
            brand_name = line.split("Brand:")[-1].strip()
            break
    print(f" Brand Name: {brand_name}")

except Exception as e :
    driver.refresh()

# ================================== Perform a search for the brand name ===============================================
# إجراء بحث عن اسم العلامة التجارية
brand_search = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id=\"customHeader\"]/div[1]/div/div[1]/div[2]/cx-page-slot/app-custom-search/div/div[2]/div[2]/input"))
)
print("تم العثور على حقل البحث")
brand_search.send_keys(brand_name, Keys.ENTER)



# ================================== Wait for the search results to load ===============================================
# انتظار تحميل نتائج البحث

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.page-item.active > a.page-link")))


# Extract Last Page
# استخراج رقم اخر صفخه
find_last_page = driver.find_elements(By.CSS_SELECTOR, "li.page-item > a.page-link")
last_page = find_last_page[-2].text



# ========================================== While Loop With count of pages ===========================================
CURRENT_PAGE = 0
while int(CURRENT_PAGE) < int(last_page) :

    # Get the current page number
    # الحصول على رقم الصفحة الحالية
    current_page_f = driver.find_element(By.CSS_SELECTOR, "li.page-item.active > a.page-link").text
    CURRENT_PAGE = current_page_f
    print(f"الصفحة الحالية هي {CURRENT_PAGE}")

    # Call external script with the current URL
    # استدعاء السكربت الخارجي باستخدام الرابط الحالي
    run_script(driver=driver, num_of_page=last_page, active_page=CURRENT_PAGE)
    print(run_script(driver, last_page, CURRENT_PAGE))



    # # Get product details from the current page
    # # استخراج تفاصيل المنتجات من الصفحة الحالية
    try:
        get_products = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".category-listing-container")))
    except Exception:
        driver.refresh()


    # Navigate to the next page
    # الانتقال إلى الصفحة التالية
    press_next = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.page-item > a.page-link[aria-label='Next']"))
    )
    press_next.click()



    # Wait for the current page to update after clicking next
    # انتظار تحديث الصفحة الحالية بعد الضغط على التالي
    current_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.page-item.active > a.page-link"))).text
    CURRENT_PAGE = current_page
    print(f"الصفحة الحالية بعد الانتقال إلى التالي: {CURRENT_PAGE}")

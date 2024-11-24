import time
from selenium.webdriver.common.by import By
from faker import Faker
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import random
"""
Script for scraping product data from the SACO website and saving it to an Excel file.

This script uses Selenium for web scraping and Pandas for managing and updating the Excel file.
It extracts product price, stock status, and product link for each item displayed on the search page.
Data is saved incrementally to an Excel file (`scraped_data.xlsx`).

Author: Mostafa Ibrahim
Date: 11-11-2024

السكربت لجلب بيانات المنتجات من موقع ساكو وحفظها في ملف Excel.

هذا السكربت يستخدم Selenium لجلب البيانات و Pandas لإدارة وتحديث ملف Excel.
يستخرج السكربت سعر المنتج، حالة توفره، ورابط المنتج لكل عنصر يظهر في صفحة البحث.
يتم حفظ البيانات بشكل متزايد في ملف Excel باسم (`scraped_data.xlsx`).
"""

def run_script(driver, active_page, num_of_page):

    # File name for storing scraped data
    # اسم الملف لتخزين البيانات المستخرجة
    fake = Faker()
    names = []
    for i in range(100):
        x = fake.name()
        names.append(x)

    r_name = random.choice(names)
    print(f"The Name of {r_name}")
    EXCEL_FILE_NAME = f"{r_name}_data.xlsx"

    # Create an empty Excel file if it doesn't already exist
    # إنشاء ملف Excel فارغ إذا لم يكن موجودًا بالفعل
    df = pd.DataFrame()
    df.to_excel(EXCEL_FILE_NAME, index=False, engine='openpyxl')

    # Initialize explicit wait
    # تهيئة الانتظار الصريح
    wait = WebDriverWait(driver, 20)

    # Wait for product elements to load
    # الانتظار حتى تحميل عناصر المنتجات
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.col-12.col-sm-6.col-md-6.col-xl-4.px-2.mb-2')))

    # Find all product elements on the page
    # العثور على جميع عناصر المنتجات في الصفحة
    product_elements = driver.find_elements(By.CSS_SELECTOR, '.col-12.col-sm-6.col-md-6.col-xl-4.px-2.mb-2')



    # List to hold scraped product data
    # قائمة لحفظ بيانات المنتجات المستخرجة
    scraped_products = []
    print(f"List Of Products: {scraped_products}")

    # Loop through each product and extract data
    # تكرار لكل منتج واستخراج البيانات
    for product_index in range(len(product_elements)):
        time.sleep(4)  # Temporary wait to avoid stale element issues
        # انتظار مؤقت لتجنب مشكلات العناصر المنتهية
        try:

            # Refresh the list of product elements
            # تحديث قائمة عناصر المنتجات
            product_elements = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.col-12.col-sm-6.col-md-6.col-xl-4.px-2.mb-2'))
            )
            current_product = product_elements[product_index]
            print(f"current index == {product_index +1}")



            # Extract price and stock status
            # استخراج السعر وحالة التوفر
            price_text = current_product.find_element(By.CLASS_NAME, 'discount-price').text.strip()
            stock_status_text = current_product.find_element(By.CLASS_NAME, 'stock-label.txt-instock').text.strip()

            # Click on the product to extract its link
            # الضغط على المنتج لاستخراج رابطه
            current_product.click()
            wait.until(EC.url_changes(driver.current_url))
            product_link = driver.current_url
            driver.back()

            # Create a dictionary of product information
            # إنشاء قاموس لمعلومات المنتج
            product_info = {
                'Price': price_text,
                'Stock Status': stock_status_text,
                'Product Link': product_link
            }
            scraped_products.append(product_info)

            # Log scraped information
            # تسجيل المعلومات المستخرجة
            print(f"Product {product_index + 1}:")
            print(f"Price: {price_text}")
            print(f"Stock Status: {stock_status_text}")
            print(f"Product Link: {product_link}")
            print("-" * 40)
            # print(scraped_products)

        except Exception as e:
            driver.refresh()
            # Refresh the list of product elements
            # تحديث قائمة عناصر المنتجات
            product_elements = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.col-12.col-sm-6.col-md-6.col-xl-4.px-2.mb-2'))
            )
            current_product = product_elements[product_index]
            print(f"current index == {product_index +1}")

            # Extract price and stock status
            # استخراج السعر وحالة التوفر
            price_text = current_product.find_element(By.CLASS_NAME, 'discount-price').text.strip()
            stock_status_text = current_product.find_element(By.CLASS_NAME, 'stock-label.txt-instock').text.strip()

            # Click on the product to extract its link
            # الضغط على المنتج لاستخراج رابطه
            current_product.click()
            wait.until(EC.url_changes(driver.current_url))
            product_link = driver.current_url
            driver.back()

            # Create a dictionary of product information
            # إنشاء قاموس لمعلومات المنتج
            product_info = {
                'Price': price_text,
                'Stock Status': stock_status_text,
                'Product Link': product_link
            }
            scraped_products.append(product_info)

            # Log scraped information
            # تسجيل المعلومات المستخرجة
            print(f"Product {product_index + 1}:")
            print(f"Price: {price_text}")
            print(f"Stock Status: {stock_status_text}")
            print(f"Product Link: {product_link}")
            print("-" * 40)
            # print(scraped_products)
            print(f"Was there an rror processing product {product_index + 1}: {str(e)}")

    # Function to update the Excel file with scraped data
    # وظيفة لتحديث ملف Excel بالبيانات المستخرجة
    def update_excel_file(data):
        """
        Updates the existing Excel file with new data.
        If the file is empty, it initializes it with the new data.

        يقوم بتحديث ملف Excel الحالي بالبيانات الجديدة.
        إذا كان الملف فارغًا، يتم تهيئته بالبيانات الجديدة.
        """
        try:
            # Load existing data from the Excel file
            # تحميل البيانات الحالية من ملف Excel
            existing_data = pd.read_excel(EXCEL_FILE_NAME)
            print(existing_data)

            # Append new data and avoid duplicates
            # إضافة البيانات الجديدة وتجنب التكرارات
            updated_data = pd.concat([existing_data, pd.DataFrame([data])], ignore_index=True)

            # Save updated data to the Excel file
            # حفظ البيانات المحدثة في ملف Excel
            updated_data.to_excel(EXCEL_FILE_NAME, index=False, engine='openpyxl')

        except Exception as e:
            print(f"Error updating Excel file: {str(e)}")

        print(f"Excel file updated successfully: {EXCEL_FILE_NAME}")


    # Extract Last Page
    # استخراج رقم اخر صفخه
    last_page = int(num_of_page)
    print(last_page)

    # Get the current page number
    # الحصول على رقم الصفحة الحالية
    current_page = int(active_page)
    print(current_page)
    print(scraped_products)


    if current_page == last_page:
        # Save each product's data to the Excel file
        # حفظ بيانات كل منتج في ملف Excel
        for product in scraped_products:
            update_excel_file(product.values())

        # Display the final Excel file path
        # عرض المسار النهائي لملف Excel
        print(f"Excel file is ready: {os.path.abspath(EXCEL_FILE_NAME)}")

    return scraped_products

# Run the script
# تشغيل السكربت
# run_script("https://www.saco.sa/en/search")

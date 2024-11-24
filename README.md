The SacoAutomationExtractor project is an automation tool developed using Selenium to scrape product data from saco.sa. The goal of this project is to simplify the collection of information like product links, prices, and availability from the website.

Features:
Scrape product data.
Support for automation of page navigation.
Extract information such as links, prices, and availability.
Save data into an Excel file.
Requirements:
To run the project, ensure the following dependencies are installed:

Python 3.x
Selenium
ChromeDriver

pip install -r requirements.txt
Ensure ChromeDriver (or the browser you choose) is downloaded and the path is updated in the code if necessary.

RUN: 
python main.py
The tool will start scraping data from the website and save it in a file.






# SacoAutomationExtractor (Selenium Scraper)

## بالعربية
مشروع **SacoAutomationExtractor** هو أداة أتمتة تم تطويرها باستخدام **Selenium** لاستخراج بيانات المنتجات من موقع **saco.sa**. الهدف من المشروع هو تسهيل جمع المعلومات مثل الروابط، الأسعار، والتوافر للمنتجات عبر الموقع.

### الميزات:
- استخراج البيانات من صفحة المنتجات.
- دعم الأتمتة للتنقل بين الصفحات.
- استخراج البيانات مثل الرابط، السعر، والتوافر.
- حفظ البيانات في ملف **Excel** أو **CSV**.

### المتطلبات:
لتشغيل المشروع، تأكد من تثبيت المتطلبات التالية:
1. Python 3.x
2. Selenium
3. ChromeDriver (أو أي متصفح آخر تدعمه Selenium)

### كيفية التثبيت:
1. قم بتنزيل المتطلبات باستخدام:
   ```bash
   pip install -r requirements.txt

تأكد من تنزيل ChromeDriver (أو المتصفح الذي تختاره) وتحديث المسار في الكود إذا لزم الأمر.
كيفية الاستخدام:
قم بتشغيل السكربت باستخدام:
'''bash
python main.py

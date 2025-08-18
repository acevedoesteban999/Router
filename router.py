from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(GeckoDriverManager().install())

options = Options()

driver = webdriver.Firefox(service=service, options=options)

try:
    driver.get("http://192.168.1.1")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "Login_Name"))
        )
        
        username = driver.find_element(By.NAME, "Login_Name")
        password = driver.find_element(By.NAME, "Login_Pwd")
        login_button = driver.find_element(By.NAME, "texttpLoginBtn")
        

        username.send_keys("admin")
        password.send_keys("admin")
        login_button.click()
        
        
    except Exception as auth_error:
        print(f"!!!!!!!!!!!!!!!!!!!!! Auth Error: {auth_error} ")
        raise
    while True:
        try:
            driver.get('http://192.168.1.1/rpSys.html')
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.NAME, "main"))
            )
            users_count = driver.find_element(By.ID, "WirelessClientNum").text
            reload_button = driver.find_element(By.NAME, "Wireless_Refresh")
        
            print(f"\n{users_count}")
            
            
            time.sleep(5)
            # driver.save_screenshot("router_status.png")
            
        except Exception as content_error:
            print(f"!!!!!!!!!!!!!!!!!!!!! Error : {content_error}")
            raise
    
except Exception as e:
    print(f"\n !!!!!!!!!!!!!!!!!!!!!Exec Error: {str(e)}")
    
finally:
    driver.quit()
    print("\nOff")
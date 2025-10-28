from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

service = Service(GeckoDriverManager().install())
options = Options()
driver = webdriver.Firefox(service=service, options=options)

RP_SYS_IP = "http://192.168.1.1"
JOOWIN_IP = "http://192.168.10.1"

try:
    #RP_SYS
    driver.get(f"{RP_SYS_IP}/rpSys.html")
    rp_sys_window = driver.current_window_handle  
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Login_Name")))

    driver.find_element(By.NAME, "Login_Name").send_keys("admin")
    driver.find_element(By.NAME, "Login_Pwd").send_keys("admin")
    driver.find_element(By.NAME, "texttpLoginBtn").click()

    
    
    
    #JOOWIN
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(JOOWIN_IP)
    joowin_window = driver.current_window_handle 
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("melon123445")
    btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@sh_lang='login']")))
    ActionChains(driver).move_to_element(btn).click().perform()

    while True:
        try:
            driver.switch_to.window(rp_sys_window)
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "main")))
            reload_button = driver.find_element(By.NAME, "Wireless_Refresh")
            reload_button.click()
                
            users_count_rp_sys = driver.find_element(By.ID, "WirelessClientNum").text
            time.sleep(1) 
            driver.switch_to.window(joowin_window)
            driver.get(f"{JOOWIN_IP}/computer/network_link.html")
            users_count_joowin = len(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "table_list"))).find_elements(By.XPATH, ".//tr"))
            print(f"\n[RP_SYS] Users: {users_count_rp_sys}")
            print(f"\n[JOOWIN] Users: {users_count_joowin}")
            time.sleep(5) 

        except Exception as loop_err:
            print(f"!!!!!!!!!!!!!!!!!!!!! Error en bucle: {loop_err}")
            raise

except Exception as e:
    print(f"\n!!!!!!!!!!!!!!!!!!!!! Exec Error: {str(e)}")

finally:
    driver.quit()
    print("\nOff")
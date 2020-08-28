from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver=webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

name='1032239178@qq.com'
password='wb123456789'
url='https://account.geetest.com/login'
driver.get(url)
driver.find_element_by_xpath(r'//*[@id="base"]/div[2]/div/div[2]/div[3]/div/form/div[1]/div/div/input').send_keys(name)
driver.find_element_by_xpath(r'//*[@id="base"]/div[2]/div/div[2]/div[3]/div/form/div[2]/div/div[1]/input').send_keys(password)
WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_radar_tip')))
driver.find_element_by_xpath(r'//*[@id="captchaIdLogin"]/div/div[2]/div[1]/div[3]').click()




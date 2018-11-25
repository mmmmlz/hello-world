from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import  ActionChains  #行为链
driver_path = r'D:\python\Scripts\chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)
driver.get('http://www.baidu.com/')
#切换窗口
driver.execute_script("window.open('http://www.douban.com')")
driver.switch_to_window(driver.window_handles[1])
print(driver.current_url)

#获取源代码
#print(driver.page_source)


#行为链
# inputTag = driver.find_element_by_id('kw')
# submitTag = driver.find_element_by_id('su')
#
# actions = ActionChains(driver)
# actions.move_to_element(inputTag)
# actions.send_keys_to_element(inputTag,'python')
# actions.move_to_element(submitTag)
# actions.click(submitTag)
# actions.perform()
#点击操作
# select_button = driver.find_element_by_name("wd")
# select_button.send_keys('python')
# select_button1 = driver.find_element_by_id("su")
# select_button1.click()


#输入框
#inputTag = driver.find_element_by_id('kw')
#inputTag.send_keys('python')
#checkbox
# inputTag = driver.find_element_by_name("remember")
# inputTag.click()

# #选择框
# from selenium.webdriver.support.ui import Select
# # 选中这个标签，然后使用Select创建对象
# selectTag = Select(driver.find_element_by_name("jumpMenu"))
# # 根据索引选择
# selectTag.select_by_index(1)
# # 根据值选择
# #.select_by_value("http://www.95yueba.com")
# # 根据可视的文本选择
# #selectTag.select_by_visible_text("95秀客户端")
# # 取消选中所有选项
# #selectTag.deselect_all()

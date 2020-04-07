from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time
class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser=webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 伊迪丝听说了一个很酷的新的看板系统。她去看它的主页。
        self.browser.get('http://localhost:8000') #打开django项目页面

        # 注意到标题显示待办事项列表，她立即进入待办事项
        self.assertIn('To-Do',self.browser.title) #断言title为‘To-Do’,并输出title
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #她在文本框中输入“购买孔雀羽毛”（伊迪丝的爱好是做飞鱼标本）
        inputbox.send_keys('Buy peacock feathers')

        #当她点击进入时，页面会更新现在页面会列出  
        # “1：购买孔雀羽毛”，作为待办事项列表中的项目
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )

        
        #接着一个文本框邀请她添加另一个项目。
        #她输入“使用孔雀羽毛制作苍蝇标本”（伊迪丝非常有条不紊）
        self.fail('Finish the test!') #测试结束~

#页面再次更新，现在在她的列表中显示这两个项目

#伊迪丝想知道该网站是否会记住她的列表。
#然后，她看到该网站为她生成了一个唯一的URL，且有一些解释性的文本。

#她访问了该网址 ，她的待办事项清单仍在那里。

#很满意，她去睡觉了。

if __name__ == '__main__':
    unittest.main(warnings='ignore')
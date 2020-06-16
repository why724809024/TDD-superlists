from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException)as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_for_one_user(self):
        # 伊迪丝听说了一个很酷的新的看板系统。她去看它的主页。
        self.browser.get(self.live_server_url)  # 打开django项目页面

        # 注意到标题显示待办事项列表，她立即进入待办事项
        self.assertIn('To-Do', self.browser.title)  # 断言title为‘To-Do’,并输出title
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 她在文本框中输入“购买孔雀羽毛”（伊迪丝的爱好是做飞鱼标本）
        inputbox.send_keys('Buy peacock feathers')

        # 当她点击进入时，页面会更新现在页面会列出
        # “1：购买孔雀羽毛”，作为待办事项列表中的项目
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # 接着一个文本框邀请她添加另一个项目。
        # 她输入“使用孔雀羽毛制作苍蝇标本”（伊迪丝非常有条不紊）
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，现在在她的列表中显示这两个项目
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')

        # 伊迪丝想知道该网站是否会记住她的列表。
        # 然后，她看到该网站为她生成了一个唯一的URL，且有一些解释性的文本。

        # 她访问了该网址 ，她的待办事项清单仍在那里。
        # self.fail('Finish the test!')  # 测试结束~
        # 很满意，她去睡觉了。

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 伊迪丝开始了一个新的to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # 她注意到她的列表有了唯一的URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # 现在一个新用户，Francis来到了这个网站

        # 我们用了一个浏览器session来确保Edith的信息不会显示出来
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis浏览主页，并未发现Edith的列表
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis 通过键入一个新item，创建了一个新列表
        # 他没有Edith那么有趣
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis得到了他自己唯一的URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 仍然，没有看到Edith的列表
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # 很满意，他也去睡觉了

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

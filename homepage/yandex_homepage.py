from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.remote.webelement import WebElement
from base.seleniumbase import SeleniumBase
class YaHomepage(SeleniumBase):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.__input_css_selector: str = 'input[name="text"][role="combobox"]'
        self.__searh_text: str = 'Тензор'
        self.__suggest_class_name: str = 'mini-suggest__popup'
        self.__first_found_css_selector: str = 'a[tabindex="0"][role="text"][target="_blank"]'
        self.__images_css_selector: str = 'a[data-statlog="services_pinned.more_popup.item.images"]'
        self.__services_css_selector: str = 'a[data-statlog="services_pinned.item.all"]'
        self.__tensor_link: str = 'http://tensor.ru/'

    def get_input_field(self) -> WebElement:
        """Return WebElement Search Bar"""
        return self.is_present('css', self.__input_css_selector, 'Search Bar is present')

    def input_text(self) -> None:
        '''Input text in Search Bar'''
        search_text = self.__searh_text
        input_text = self.is_visible('css', self.__input_css_selector)
        input_text.clear()
        input_text.send_keys(search_text)

    def get_visible_mini_suggest(self) -> WebElement:
        '''Return WebElement mini_suggest if it visible'''
        return self.is_visible('class_name', self.__suggest_class_name, 'Mini-suggest__popup is visible')

    def input_text_enter(self) -> None:
        '''Input Enter in Search Bar'''
        input_text = self.is_visible('css', self.__input_css_selector)
        input_text.send_keys(Keys.ENTER)

    def first_found_element(self) -> WebElement:
        '''Return first found WebElement'''
        return self.is_present('css', self.__first_found_css_selector, 'Element exist')

    def validate_element_link(self, element: WebElement) -> bool:
        '''Validate link first found WebElement'''
        return element.get_attribute('href') == self.__tensor_link

    def get_menu_pictures(self) -> WebElement:
        """Return WebElement 'Картинки'"""
        self.is_present('css', self.__services_css_selector, 'Pictures is present').click()
        return self.is_present('css', self.__images_css_selector, 'Pictures is present')

    def hover(self, find_by: str, locator: str):
        element_to_hover_over = self.is_present(find_by, locator)
        hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
        hover.perform()
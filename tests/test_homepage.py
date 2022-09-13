import pytest
from homepage.yandex_homepage import YaHomepage
from loguru import logger

logger.add("debug.json", format="{time}{level}{message}", level="DEBUG", rotation="100 KB", compression="zip",
           serialize=True)


@pytest.mark.usefixtures('setup')
class TestHomepage:

    @logger.catch
    def test_search_input(self):
        ''' 1)	Зайти на ya.ru
            2)	Проверить наличия поля поиска'''

        yh = YaHomepage(self.driver)
        yh.get_input_field()

    @logger.catch
    def test_visible_mini_suggest(self):
        ''' 3)	Ввести в поиск Тензор
            4)	Проверить, что появилась таблица с подсказками (suggest) '''
        yh = YaHomepage(self.driver)
        yh.get_input_field()
        yh.input_text()
        yh.get_visible_mini_suggest()

    @logger.catch
    def test_validate_element_link(self):

        ''' 5)	При нажатии Enter появляется таблица результатов поиска
            6)	Проверить 1 ссылка ведет на сайт tensor.ru '''

        yh = YaHomepage(self.driver)
        yh.get_input_field()
        yh.input_text()
        yh.input_text_enter()
        assert yh.validate_element_link(yh.first_found_element())

    @logger.catch
    def test_search_menu_pictures(self):

        ''' 1)	Зайти на ya.ru
            2)	Проверить, что ссылка «Картинки» присутствует на страниц'''

        yh = YaHomepage(self.driver)
        yh.get_menu_pictures()

    @logger.catch
    def test_href_menu_pictures(self):

        ''' 3)	Кликаем на ссылку
            4)	Проверить, что перешли на url https://yandex.ru/images'''

        yh = YaHomepage(self.driver)
        yh.get_menu_pictures().click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        link = self.driver.current_url
        assert link == 'https://yandex.ru/images/'

    @logger.catch
    def test_images_service(self):
        ''' 5)	Открыть первую категорию
            6)	Проверить, что название категории отображается в поле поиска
            7)	Открыть 1 картинку
            8)	Проверить, что картинка открылась
            9)	Нажать кнопку вперед
            10.	Проверить, что картинка сменилась
            11.	Нажать назад
            12.	Проверить, что картинка осталась из шага 8 '''
        yh = YaHomepage(self.driver)
        yh.driver.get('https://yandex.ru/images/')
        first_category = yh.is_present('css', 'div[class="PopularRequestList-Item PopularRequestList-Item_pos_0"]', '')
        first_category_text = first_category.get_attribute('data-grid-text')
        href = yh.is_present('css', 'a[class="Link PopularRequestList-Preview"]', '')
        href.click()
        search_category_text = yh.is_present('css', 'input[name="text"]', '').get_attribute('value')
        assert search_category_text == first_category_text
        yh.is_present('css', 'a[class="serp-item__link"]', '').click()
        yh.hover('css', 'img[class="MMImage-Origin"]')
        first_image_origin_url = yh.is_present('css', 'img[class="MMImage-Origin"]', '').get_attribute('src')
        yh.is_present('css', 'div[class="CircleButton CircleButton_type_next CircleButton_type MediaViewer-Button '
                             'MediaViewer-Button_hovered MediaViewer_theme_fiji-Button MediaViewer-ButtonNext '
                             'MediaViewer_theme_fiji-ButtonNext"]', '').click()
        second_image_origin_url = yh.is_present('css', 'img[class="MMImage-Origin"]', '').get_attribute('src')
        assert first_image_origin_url != second_image_origin_url
        yh.hover('css', 'img[class="MMImage-Origin"]')
        yh.is_present('css', 'div[class="CircleButton CircleButton_type_prev CircleButton_type MediaViewer-Button '
                             'MediaViewer_theme_fiji-Button MediaViewer-ButtonPrev '
                             'MediaViewer_theme_fiji-ButtonPrev"]', '').click()
        previous_image_origin_url = yh.is_present('css', 'img[class="MMImage-Origin"]', '').get_attribute('src')
        assert first_image_origin_url == previous_image_origin_url

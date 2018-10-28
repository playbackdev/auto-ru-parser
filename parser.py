'''
Парсер с помощью Silenium со  страницы со списком нужных машин (в данном случае поставлены фильтры  на Volkswagen Jetta VI поколения с сортировкой по возрастанию цены) на auto.ru
достает и выводит в консоль информацию по пробегу, году выпуска и номеру телефона владельца всех найденных автомобилей.
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Bot:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.navigate()

    def navigate(self):
        self.driver.get('https://auto.ru/moskovskaya_oblast/cars/all/?mark_model_nameplate=VOLKSWAGEN%23JETTA%23%237355324&mark_model_nameplate=VOLKSWAGEN%23JETTA%23%2320251644&transmission=AUTOMATIC&sort=price-asc')

        #Закрываем всплывающую рекламу если она есть
        try:
            popup_element = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, '//span[@class="Link PromoPopupHistory__body-link"]')))
        except:
            popup_element = None;

        if(popup_element != None):
            button_promo = self.driver.find_element_by_xpath('//span[@class="Link PromoPopupHistory__body-link"]')
            button_promo.click()

        href = []

        while 1==1:
            # проверка на кликабельность кнопки следующей страницы
            try:
                button_nextpage = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="Button Button_color_white Button_size_s Button_type_link Button_width_default ListingPagination-module__next"]')))
            except:
                button_nextpage = None

            #Находим все машины на текущей странице и записываем ссылки в массив
            items = self.driver.find_elements_by_xpath('//a[@class="Link ListingItemTitle-module__link"]')
            for i in range(len(items)):
                href.append(items[i].get_attribute('href'))


            if(button_nextpage != None):
                # уходим на следующую страницу
                button_nextpage = self.driver.find_element_by_xpath('//a[@class="Button Button_color_white Button_size_s Button_type_link Button_width_default ListingPagination-module__next"]')
                href_nextpage = button_nextpage.get_attribute('href')
                self.driver.get(href_nextpage)
            else:
                # страниц больше нет, прерываем цикл
                break

        print('Всего найдено автомобилей:' + str(len(href)))

        # цикл по записанным страницам для записи данных о машине
        for i in range(len(href)):
            self.driver.get(href[i])
            # выводим ссылку
            print(href[i])
            # выводим год выпуска
            div = self.driver.find_element_by_xpath('//div[@class="CardInfo-module__CardInfo__row CardInfo-module__CardInfo__row_year CardInfo-module__CardInfo__row_bold"]')
            print(div.text)
            # выводим пробег
            div = self.driver.find_element_by_xpath('//div[@class="CardInfo-module__CardInfo__row CardInfo-module__CardInfo__row_bold"]')
            print(div.text)
            # получаем номер телефона владельца
            button_show_phone = self.driver.find_element_by_xpath('//div[@class="CardPhone-module__phone CardOwner-module__phone CardPhone-module__preview"]')
            button_show_phone.click()

            try:
                phone_menu = WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="SellerPhonePopup-module__phoneNumber"]')))
            except:
                phone_menu = None;

            if (phone_menu != None):
                div = self.driver.find_element_by_xpath('//div[@class="SellerPhonePopup-module__phoneNumber"]')
                print(div.text)




def main():
    b = Bot()

if __name__ == '__main__':
    main()
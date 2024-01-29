import time

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(4)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:

    #Direccion
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    #Abrir el formulario de reserva
    order_a_taxi_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    comfort_tariff_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    comfort_card = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]')

    #Agregar un numero de telefono
    phone_button = (By.CLASS_NAME, 'np-button')
    phone_number_form = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]')
    phone_container = (By.ID, 'phone')
    next_button = (By.CSS_SELECTOR, "#root > div > div.number-picker.open > div.modal > div.section.active > form > div.buttons > button")
    phone_code_form = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]')
    phone_code_field = (By.ID, 'code')
    confirm_phone_code_button = (By.XPATH, "//div[text()='Confirmar']")

    #Agregar una tarjeta de credito
    payment_method_container = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]')
    payment_method_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]')
    add_a_credit_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]')
    new_credit_card_form = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]')
    card_number_field = (By.ID, 'number')
    credit_card_code_field = (By.CSS_SELECTOR, '#code')
    link_button = (By.XPATH, "//div[text()='Enlace']")

    #Agregar un comentario para el conductor
    comment_field = (By.ID, 'comment')

    #Requisitos del pedido
    requirements_display = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]')
    blanket_and_scarves_toggle_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[2]/div/div[2]/div/span')
    icecream_counter_plus = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    icecream_counter_value = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]')

    #Reservar un taxi
    book_a_taxi_button = (By.CLASS_NAME, 'smart-button-wrapper')
    wait_for_a_driver_screen = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[2]')
    order_shown = (By.CLASS_NAME, 'order shown')

    def __init__(self, driver):
        self.driver = driver
        self.phone_number = None

    # Direccion
    def set_route(self, from_address, to_address):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    # Abrir el formulario de reserva

    def click_order_a_taxi_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.order_a_taxi_button))
        self.driver.find_element(*self.order_a_taxi_button).click()

    def click_comfort_tariff(self):
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.comfort_tariff_button))
        self.driver.find_element(*self.comfort_tariff_button).click()

    def is_comfort_tariff_displayed(self):
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(self.comfort_card))
        return self.driver.find_element(*self.comfort_card).is_displayed()

    # Agregar un numero de telefono
    def click_phone_number(self):
        self.driver.find_element(*self.phone_button).click()

    def set_phone_number(self, phone_number):
        data.phone_number = phone_number
        self.driver.find_element(*self.phone_container).send_keys(phone_number)

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_container).get_property('value')

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

    def set_phone_code(self):
        phone_code = retrieve_phone_code(self.driver)
        self.driver.find_element(self.phone_code_field).send_keys(str(phone_code))

    def get_phone_code(self):
        time.sleep(3)
        return self.driver.find_element(*self.phone_code_field).get_property('value')

    def click_confirm_phone_code_button(self):
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.confirm_phone_code_button))
        self.driver.find_element(*self.confirm_phone_code_button).click()
        time.sleep(2)

    # Agregar una tarjeta de credito
    def click_payment_method(self):
        self.driver.find_element(*self.payment_method_container).click()

    def is_payment_method_card_displayed(self):
        return self.driver.find_element(*self.payment_method_card).is_displayed()

    def click_add_a_new_card(self):
        self.driver.find_element(*self.add_a_credit_card).click()

    def is_add_a_new_credit_card_form_displayed(self):
        return self.driver.find_element(*self.new_credit_card_form).is_displayed()

    def set_a_new_card(self, card_number, card_code):
        self.driver.find_element(*self.card_number_field).send_keys(card_number)
        time.sleep(2)
        self.driver.find_element(*self.credit_card_code_field).send_keys(card_code)
        time.sleep(2)
        self.driver.find_element(*self.credit_card_code_field).send_keys(Keys.TAB)

    def get_credit_card_number(self):
        return self.driver.find_element(*self.card_number_field).get_property('value')

    def get_credit_card_code(self):
        return self.driver.find_element(*self.credit_card_code_field).get_property('value')

    def click_link_button(self):
        self.driver.find_element(*self.link_button).click()
        time.sleep(2)

    # Agregar un comentario para el conductor

    def set_comment(self, message_for_driver):
        self.driver.find_element(*self.comment_field).send_keys(message_for_driver)

    def get_comment(self):
        return self.driver.find_element(*self.comment_field).get_property('value')

    # Requisitos del pedido

    def click_requirements_display(self):
        self.driver.find_element(*self.requirements_display).click()

    def click_blanket_and_scarves_toggle_button(self):
        self.driver.find_element(*self.blanket_and_scarves_toggle_button).click()

    def is_blanket_and_scarves_selected(self):
        return self.driver.find_element(*self.blanket_and_scarves_toggle_button).is_selected()

    def click_add_2_icecream(self):
        self.driver.find_element(*self.icecream_counter_plus).click()
        self.driver.find_element(*self.icecream_counter_plus).click()

    def get_icecream_counter(self):

        return self.driver.find_element(*self.icecream_counter_value).get_property('value')

    #Reservar un taxi
    def click_book_a_taxi_button(self):
        self.driver.find_element(*self.book_a_taxi_button).click()

    def is_wait_for_a_driver_screen_displayed(self):
        return self.driver.find_element(*self.wait_for_a_driver_screen).is_displayed()

    def wait_for_load_order(self):
        WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located(self.order_shown))

    def is_order_screen_displayed(self):
        return self.driver.find_element(*self.order_shown).is_displayed()

class TestUrbanRoutes:

    driver = None
    routes_page = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        cls.driver = webdriver.Chrome()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("perfLoggingPrefs", {'enableNetwork': True, 'enablePage': True})
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    #Pide un taxi con la tarifa comfort y comprueba que el formulario de dicha tarifa este presente
    def test_select_comfort_tariff(self):
        self.routes_page.click_order_a_taxi_button()
        self.routes_page.click_comfort_tariff()
        assert self.routes_page.is_comfort_tariff_displayed()

    #Abre el formulario de telefono, rellena el campo
    #Comprueba que el numero que la aplicacion recibe sea igual al enviado

    def test_set_phone_number(self):
        self.routes_page.click_phone_number()
        self.routes_page.set_phone_number(data.phone_number)
        self.routes_page.get_phone_number()
        phone_number = data.phone_number
        assert self.routes_page.get_phone_number() == phone_number
        self.routes_page.click_next_button()


    #Recibe el codigo de telefono, lo envia y comprueba que no esta vacio
    def test_set_phone_code(self):
        # Establecer el código
        self.routes_page.set_phone_code()

         #Obtener el código establecido
        phone_code = self.routes_page.get_phone_code()

         #Esperar hasta que el código sea visible (ajusta según sea necesario)
        WebDriverWait(self.driver, timeout=10).until(
           EC.text_to_be_present_in_element_value(self.routes_page.phone_code_field, phone_code)
        )

         #Obtener el código después de la espera
        code_after_wait = self.routes_page.get_phone_code()
         #Verificar si el código antes y después de la espera es el mismo
        assert phone_code == code_after_wait
        assert code_after_wait is not None
        assert str(code_after_wait) != 'None'
        self.routes_page.click_confirm_phone_code_button()

    #Llena los campos para añadir una nueva tarjeta y confirma que la pagina reciba los datos
    def test_set_a_new_card_data(self):
        self.routes_page.click_payment_method()
        self.routes_page.click_add_a_new_card()
        self.routes_page.set_a_new_card(data.card_number, data.card_code)
        self.routes_page.get_credit_card_number()
        self.routes_page.get_credit_card_code()
        assert self.routes_page.get_credit_card_number() == data.card_number
        assert self.routes_page.get_credit_card_code() == data.card_code
        self.routes_page.click_link_button()


    #Comprueba que se pueda añadir un comentario
    def test_set_comment(self):
        self.routes_page.set_comment(data.message_for_driver)
        self.routes_page.get_comment()
        assert self.routes_page.get_comment() == data.message_for_driver

    #Comprueba que el toggle button de manta y pañuelos quede seleccionado despues de
    #click en el
    def test_add_blanket_and_scarves(self):
        self.routes_page.click_requirements_display()
        self.routes_page.click_blanket_and_scarves_toggle_button()
        assert self.routes_page.is_blanket_and_scarves_selected()

    #Comprueba que el contador de helados sea igual a 2 despues de dar click 2 veces en
    #el boton '+'
    def test_add_2_icecream(self):
        self.routes_page.click_add_2_icecream()
        assert self.routes_page.get_icecream_counter() == 2

    def test_book_a_taxi(self):
         self.routes_page.click_book_a_taxi_button()
         assert self.routes_page.is_wait_for_a_driver_screen_displayed()
         self.routes_page.wait_for_load_order()
         assert self.routes_page.is_order_screen_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

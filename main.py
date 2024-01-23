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
            time.sleep(1)
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
    phone_code_field = (By.CLASS_NAME, "input container")
    confirm_phone_code_button = (By.XPATH, "//div[text()='Confirmar']")

    #Agregar una tarjeta de credito
    payment_method_container = (By.CLASS_NAME, 'pp-button filled')
    add_a_credit_card = (By.CLASS_NAME, 'pp-row disabled')
    card_number_field = (By.ID, 'number')
    credit_card_code_field = (By.ID, 'code')
    link_button = (By.XPATH, "//div[text()='Enlace']")

    #Agregar un comentario para el conductor
    comment_field = (By.ID, 'comment')

    #Requisitos del pedido
    blanket_and_scarves_toggle_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[2]/div/div[2]/div/span')
    icecream_toggle_button =(By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')

    #Reservar un taxi
    book_a_taxi_button = (By.CLASS_NAME, 'smart-button-wrapper')
    order_shown = (By.CLASS_NAME, 'order shown')

    def __init__(self, driver):
        self.driver = driver

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
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.order_a_taxi_button))
        self.driver.find_element(*self.order_a_taxi_button).click()

    def click_comfort_tariff(self):
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.comfort_tariff_button))
        self.driver.find_element(*self.comfort_tariff_button).click()

    def is_comfort_tariff_displayed(self):
        return self.driver.find_element(*self.comfort_card).is_displayed()

    # Agregar un numero de telefono

    def click_phone_number(self):
        self.driver.find_element(*self.phone_button).click()

    def is_phone_number_form_displayed(self):
        return self.driver.find_element(*self.phone_number_form).is_displayed()

    def set_phone_number(self, phone_number):
        data.phone_number = phone_number
        self.driver.find_element(*self.phone_container).send_keys(phone_number)

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_container).get_property('value')

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

    def is_phone_code_form_displayed(self):
        return self.driver.find_element(*self.phone_code_form).is_displayed()

    def set_phone_code(self):
        code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.phone_code_field).send_keys(code)

    def get_phone_code(self):
        return self.driver.find_element(*self.phone_code_field).get_property('value')

    def click_confirm_phone_code_button(self):
        self.driver.find_element(*self.confirm_phone_code_button).click()

    # Agregar una tarjeta de credito

    def click_payment_method(self):
        self.driver.find_element(*self.payment_method_container).click()

    def click_add_a_new_card(self):
        self.driver.find_element(*self.add_a_credit_card).click()

    def set_card_number(self, card_number):
        self.driver.find_element(*self.card_number_field).send_keys(card_number)

    def get_card_number(self):
        return self.driver.find_element(*self.card_number_field).get_property('value')

    def set_credit_card_code(self, card_code):
        self.driver.find_element(*self.credit_card_code_field).send_keys(card_code)
        card_code.send_keys(Keys.TAB)

    def get_credit_card_code(self):
        return self.driver.find_element(*self.credit_card_code_field).get_property('value')

    def click_link_button(self):
        self.driver.find_element(*self.link_button).click()

    # Agregar un comentario para el conductor

    def set_comment(self, message_for_driver):
        self.driver.find_element(*self.comment_field).send_keys(message_for_driver)

    def get_comment(self):
        return self.driver.find_element(*self.comment_field).get_property('value')

    # Requisitos del pedido
    def click_blanket_and_scarves_toggle_button(self):
        self.driver.find_element(*self.blanket_and_scarves_toggle_button).click()

    def click_icecream_toggle_button(self):
        self.driver.find_element(*self.icecream_toggle_button).click()
        self.driver.find_element(*self.icecream_toggle_button).click()

    #Reservar un taxi
    def click_book_a_taxi_button(self):
        self.driver.find_element(*self.book_a_taxi_button).click()

    def wait_for_load_order(self):
        WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located(self.order_shown))
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

    # Da click en el boton Siguiente y comprueba que avance al siguiente formulario
    def test_is_phone_code_form_displayed(self):
        self.routes_page.click_next_button()
        WebDriverWait(self.driver, 3)
        assert self.routes_page.is_phone_code_form_displayed()

    #Recibe el codigo de telefono, lo envia y comprueba que no esta vacio
    def test_set_phone_code(self):
        self.routes_page.set_phone_code()
        self.routes_page.get_phone_code()
        WebDriverWait(self.driver, 3)
        assert self.routes_page.get_phone_code() is not None

    #Da click en el boton para confirmar el codigo de telefono y confirma que los 2 formularios anteriores se cierren
    def test_confirm_phone_code_button(self):
        self.routes_page.click_confirm_phone_code_button()
        WebDriverWait(self.driver, 3)
        assert self.routes_page.is_phone_code_form_displayed() == False
        assert self.routes_page.is_phone_number_form_displayed() == False




    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

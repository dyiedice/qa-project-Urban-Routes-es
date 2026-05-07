from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import data
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
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    confort_plan= (By.XPATH,"//div[contains(@class, 'taxis')]//div[text()='Comfort']")



    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.to_field))
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)



class TestUrbanRoutes:
    driver = None


    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        cls.driver = webdriver.Chrome(options=chrome_options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_set_confort(self):
        self.test_set_route()

        #Entrar al boton de pedir un taxi
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Pedir un taxi')]"))
        )
        button.click()

        #seleccionar el plan comfort
        confort_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='tcard-title' and text()='Comfort']"))
        )
        confort_button.click()
        #Verificar que se activo
        assert confort_button.is_enabled(), "La tarjeta Comfort no está habilitada"

    def test_set_telefonic_number(self):
            self.test_set_confort()

            # Abrir formulario
            label_access_number_formulary = self.driver.find_element(
                By.XPATH, "//div[@class='np-text' and text()='Número de teléfono']"
            )
            label_access_number_formulary.click()

            # Esperar el input y escribir el número
            input_number = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@id='phone' and @class='input']"))
            )
            input_number.send_keys(data.phone_number)

            # Verificar que el número fue ingresado
            assert input_number.get_attribute("value") == data.phone_number, "El número no coincide"

            # Enviar el formulario
            button_submit_number = self.driver.find_element(
                By.XPATH, "//button[@class='button full' and contains(text(),'Siguiente')]"
            )
            button_submit_number.click()

            #Obtener el codigo y ponerlo en el input
            input_code =  WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='code' and @class='input']"))
            )
            input_code.send_keys(retrieve_phone_code(self.driver))
            self.driver.find_element(By.XPATH, '//button[@class="button full" and contains(text(), "Confirmar")]').click()

            # Assert para verificar que el numero sea igual al de data
            assert label_access_number_formulary.text == data.phone_number

    def test_add_credit_card(self):
        self.test_set_confort()

        #acceder al formulario de tipo de pago
        payment_method= WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='pp-text' and text()='Método de pago']"))
        )
        payment_method.click()

        #añadir la tarjeta
        add_card_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']"))
        )
        add_card_button.click()

        #añade los numeros de la tarjeta
        config_numbers_card=WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='number' and @class='card-input']"))
        )
        config_numbers_card.send_keys(data.card_number)

        #añade el codigo de la tarjeta
        config_code_card= self.driver.find_element(By.XPATH, "//input[@id='code' and @class='card-input']")
        config_code_card.send_keys(data.card_code)

        #Da click al boton agregar
        config_code_card.send_keys(Keys.TAB)
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='button full' and contains(text(), 'Agregar')]"))
        )
        submit_button.click()

        #Verifica si se agregó
        checkbox_card_method= WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,"//input[@id='card-1' and @class='checkbox']"))
            )
        assert checkbox_card_method.is_selected(), 'no se agregó'

    def test_add_driver_message(self):
        self.test_set_confort()
        message_label= WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='comment' and @class='input']")))
        message_label.send_keys(data.message_for_driver)
        assert message_label.get_attribute("value")== data.message_for_driver, "El mensaje no coincide"
    def test_add_blanket_(self):
        self.test_set_confort()
        add_blanket = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='slider round']"))
        )
        add_blanket.click()
        print('Se selecciono correctamente')
    def test_add_ice_cream(self):
        self.test_set_confort()
        add_ice_cream = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='counter-plus']"))
        )
        add_ice_cream.click()
        add_ice_cream.click()
        assert self.driver.find_element(By.XPATH, "//div[@class=counter-value]")==2
    def test_taxi_module(self):
        self.test_set_route()
        # Entrar al boton de pedir un taxi
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Pedir un taxi')]"))
        )
        button.click()

        # seleccionar el plan comfort
        confort_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='tcard-title' and text()='Glamuroso']"))
        )
        confort_button.click()

        # Abrir formulario
        label_access_number_formulary = self.driver.find_element(
            By.XPATH, "//div[@class='np-text' and text()='Número de teléfono']"
        )
        label_access_number_formulary.click()

        # Esperar el input y escribir el número
        input_number = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='phone' and @class='input']"))
        )
        input_number.send_keys(data.phone_number)

        # Verificar que el número fue ingresado
        assert input_number.get_attribute("value") == data.phone_number, "El número no coincide"

        # Enviar el formulario
        button_submit_number = self.driver.find_element(
            By.XPATH, "//button[@class='button full' and contains(text(),'Siguiente')]"
        )
        button_submit_number.click()

        # Obtener el codigo y ponerlo en el input
        input_code = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='code' and @class='input']"))
        )
        input_code.send_keys(retrieve_phone_code(self.driver))
        self.driver.find_element(By.XPATH, '//button[@class="button full" and contains(text(), "Confirmar")]').click()

        #Ahora si dar click al pedir taxi
        get_taxi= WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@class="smart-button-main"]'))
        )
        get_taxi.click()
        assert self.driver.find_element(By.XPATH,'//div[@class="order-body"]').is_displayed()
    def test_wait_driver(self):
        self.test_taxi_module()
        driver_text = WebDriverWait(self.driver, 120).until(
            EC.visibility_of_element_located((By.XPATH,  "//div[@class='order-header-content']//div[@class='order-number']"))
        )
        assert driver_text.is_displayed()




    @classmethod
    def teardown_class(cls):
        cls.driver.quit()




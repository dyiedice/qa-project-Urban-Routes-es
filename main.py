from selenium import webdriver
import data
from pages import UrbanRoutesPage

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
        self.routes_page = UrbanRoutesPage(self.driver)
        self.test_set_route()
        self.routes_page.button_get_taxi()
        self.routes_page.set_confort_plan()
        #Verificar que se activo
        assert self.routes_page.set_confort_plan().is_enabled(), "La tarjeta Comfort no está habilitada"

    def test_set_telefonic_number(self):
            self.routes_page = UrbanRoutesPage(self.driver)
            self.test_set_confort()
            # Abrir formulario
            self.routes_page.open_number_formulary()

            # Esperar el input y escribir el número
            self.routes_page.label_number_data_key()

            # Verificar que el número fue ingresado
            assert self.routes_page.label_number().get_attribute("value") == data.phone_number, "El número no coincide"

            # Enviar el formulario
            self.routes_page.button_submit_number()

            #Obtener el codigo y ponerlo en el input
            self.routes_page.input_code()
            self.routes_page.input_code_retrieved()
            self.routes_page.button_submit_code()

            # Assert para verificar que el numero sea igual al de data
            assert self.routes_page.assert_saved_number() == data.phone_number

    def test_add_credit_card(self):
            self.test_set_confort()
            self.routes_page = UrbanRoutesPage(self.driver)
            #acceder al formulario de tipo de pago
            self.routes_page.open_payment_form()
            self.routes_page.add_card_form()
            #añade los numeros de la tarje1ta
            self.routes_page.card_numbers_send_key()

            #añade el codigo de la tarjeta
            self.routes_page.card_code_sendkeys()

            #Da click al boton agregar
            self.routes_page.submit_card_form()

            #Verifica si se agregó
            assert self.routes_page.assert_checkbox().is_selected(), 'no se agregó'

    def test_add_driver_message(self):
        self.test_set_confort()
        self.routes_page = UrbanRoutesPage(self.driver)
        self.routes_page.label_message_for_driver().send_keys(data.message_for_driver)
        assert self.routes_page.label_message_for_driver().get_attribute("value")== data.message_for_driver, "El mensaje no coincide"
    def test_add_blanket_(self):
        self.test_set_confort()
        self.routes_page = UrbanRoutesPage(self.driver)
        self.routes_page.add_blanket_()
        assert self.routes_page.assert_checkbox_blanket().get_attribute("checked") == "true",  "Manta y pañuelos no está activado"
    def test_add_ice_cream(self):
        self.test_set_confort()
        self.routes_page = UrbanRoutesPage(self.driver)
        self.routes_page.add_ice_2_clicks()
        assert self.routes_page.ice_cream_counter().text == "2"

    def test_taxi_module(self):
        self.test_set_route()
        self.routes_page = UrbanRoutesPage(self.driver)
        self.routes_page.button_get_taxi()
        self.routes_page.set_glamorous_plan()
            # Abrir formulario
        self.routes_page.open_number_formulary()

        # Esperar el input y escribir el número
        self.routes_page.label_number_data_key()

        # Verificar que el número fue ingresado
        assert self.routes_page.label_number().get_attribute("value") == data.phone_number, "El número no coincide"

        # Enviar el formulario
        self.routes_page.button_submit_number()

        # Obtener el codigo y ponerlo en el input
        self.routes_page.input_code()
        self.routes_page.input_code_retrieved()
        self.routes_page.button_submit_code()

        #Ahora si dar click al pedir taxi
        self.routes_page.final_get_taxi()
        assert self.routes_page.assert_taxi_module().is_displayed()
    def test_wait_driver(self):
        self.test_taxi_module()
        assert self.routes_page.driver_module_text().is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()




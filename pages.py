
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys
import helpers
import data

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
    def button_get_taxi(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Pedir un taxi')]"))
        )
        button.click()
    def set_confort_plan(self):
        confort_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='tcard-title' and text()='Comfort']"))
        )
        confort_button.click()
        return confort_button
    def set_glamorous_plan(self):
         WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='tcard-title' and text()='Glamuroso']"))
        ).click()
    def open_number_formulary(self):
        return self.driver.find_element(
            By.XPATH, "//div[@class='np-text']"
        ).click()

    def label_number(self):
        input_number = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='phone' and @class='input']"))
        )
        return input_number
    def label_number_data_key(self):
        self.label_number().send_keys(data.phone_number)
    def button_submit_number(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='button full' and contains(text(),'Siguiente')]"))
        ).click()
    def input_code(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='code' and @class='input']"))
        )
    def input_code_retrieved(self):
        self.input_code().send_keys(helpers.retrieve_phone_code(self.driver))

    def button_submit_code(self):
         self.driver.find_element(By.XPATH, '//button[@class="button full" and contains(text(), "Confirmar")]').click()
    def assert_saved_number(self):
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//div[@class='np-text']"), "+1")
        )
        return self.driver.find_element(By.XPATH, "//div[@class='np-text']").text
    def open_payment_form(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='pp-text' and text()='Método de pago']"))
        ).click()
    def add_card_form(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']"))
        ).click()
    def card_numbers_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='number' and @class='card-input']"))
        )
    def card_numbers_send_key(self):
        self.card_numbers_input().send_keys(data.card_number)
    def card_code_input(self):
        return self.driver.find_element(By.XPATH, "//input[@id='code' and @class='card-input']")

    def card_code_sendkeys(self):
        self.card_code_input().send_keys(data.card_code)
        self.card_code_input().send_keys(Keys.TAB)
    def submit_card_form(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='button full' and contains(text(), 'Agregar')]"))
        ).click()
    def assert_checkbox(self):
         return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='card-1' and @class='checkbox']"))
        )
    def label_message_for_driver(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='comment' and @class='input']")))

    def add_blanket_(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='slider round']"))
        ).click()
    def assert_checkbox_blanket(self):
        return self.driver.find_element(
            By.XPATH, "//input[@type='checkbox' and @class='switch-input']"
        )
    def add_ice_cream_(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='counter-plus']"))
        )
    def add_ice_2_clicks(self):
        self.add_ice_cream_().click()
        self.add_ice_cream_().click()

    def ice_cream_counter(self):
        return self.driver.find_element(By.XPATH, "//div[@class='counter-value']")
    def final_get_taxi(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@class="smart-button-main"]'))
        ).click()
    def assert_taxi_module(self):
        return self.driver.find_element(By.XPATH, '//div[@class="order-body"]')
    def driver_module_text(self):
         return WebDriverWait(self.driver, 120).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='order-header-content']//div[@class='order-number']"))
        )





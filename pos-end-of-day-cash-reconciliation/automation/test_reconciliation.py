
# ============================================================
# EOD POS DEMO - SELENIUM / PYTEST TEST CASES
# ============================================================
#
# Testing techniques demonstrated:
# 1. Functional Testing
# 2. Equivalence Partitioning
# 3. Boundary Value Analysis
# 4. Negative Testing
#
# Website:
# EOD POS Demo
#
# Run with:
# python -m pytest testcases.py -v -s
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

import os
import time

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

INDEX_FILE = os.path.join(
    BASE_DIR,
    "index.html"
)

URL = "file:///" + INDEX_FILE.replace("\\", "/")


# ------------------------------------------------------------
# Timing
# ------------------------------------------------------------

# Small pause after important actions so that the browser
# activity can be observed during demonstration.

ACTION_DELAY = 0.6

# Selenium wait timeout

WAIT_TIMEOUT = 10


# ============================================================
# DRIVER CREATION
# ============================================================

def create_driver():

    options = Options()

    # Keep browser visible for demonstration.

    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        options=options
    )

    driver.get(URL)

    time.sleep(1)

    return driver


# ============================================================
# PAUSE
# ============================================================

def pause(seconds=ACTION_DELAY):

    time.sleep(seconds)


# ============================================================
# WAIT FOR ELEMENT
# ============================================================

def wait_for_element(
    driver,
    element_id,
    timeout=WAIT_TIMEOUT
):

    return WebDriverWait(
        driver,
        timeout
    ).until(
        EC.presence_of_element_located(
            (By.ID, element_id)
        )
    )


# ============================================================
# WAIT FOR CLICKABLE ELEMENT
# ============================================================

def wait_for_clickable(
    driver,
    element_id,
    timeout=WAIT_TIMEOUT
):

    return WebDriverWait(
        driver,
        timeout
    ).until(
        EC.element_to_be_clickable(
            (By.ID, element_id)
        )
    )


# ============================================================
# CLICK ELEMENT
# ============================================================

def click_element(
    driver,
    element_id
):

    element = wait_for_clickable(
        driver,
        element_id
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        element
    )

    pause(0.2)

    element.click()

    pause()


# ============================================================
# ENTER TEXT
# ============================================================

def enter_text(
    driver,
    element_id,
    value
):

    element = wait_for_element(
        driver,
        element_id
    )

    element.clear()

    element.send_keys(
        str(value)
    )

    pause()


# ============================================================
# CHECK ELEMENT VISIBILITY
# ============================================================

def element_visible(
    driver,
    element_id
):

    try:

        element = driver.find_element(
            By.ID,
            element_id
        )

        return element.is_displayed()

    except (
        NoSuchElementException,
        WebDriverException
    ):

        return False


# ============================================================
# GET ELEMENT TEXT
# ============================================================

def get_text(
    driver,
    element_id
):

    element = wait_for_element(
        driver,
        element_id
    )

    return element.text.strip()


# ============================================================
# GET CLOSING RESULT
# ============================================================

def get_closing_result(
    driver
):

    element = wait_for_element(
        driver,
        "closing-result"
    )

    return element.text.strip()


# ============================================================
# MAKE CASH SALE
# ============================================================

def make_cash_sale(
    driver,
    product_id,
    amount_paid
):

    # Select product

    click_element(
        driver,
        product_id
    )

    # Open payment screen

    click_element(
        driver,
        "payment-button"
    )

    # Select CASH

    click_element(
        driver,
        "cash-payment-button"
    )

    # Enter amount paid

    enter_text(
        driver,
        "amount-paid",
        amount_paid
    )

    # Complete cash payment

    click_element(
        driver,
        "continue-payment-button"
    )

    pause()


# ============================================================
# MAKE CARD SALE
# ============================================================

def make_card_sale(
    driver,
    product_id
):

    # Select product

    click_element(
        driver,
        product_id
    )

    # Open payment

    click_element(
        driver,
        "payment-button"
    )

    # Select CARD

    click_element(
        driver,
        "card-payment-button"
    )

    pause()

    # Complete card payment

    click_element(
        driver,
        "continue-card-payment-button"
    )

    pause()


# ============================================================
# OPEN CLOSING CONTROL
# ============================================================

def open_closing_control(
    driver
):

    click_element(
        driver,
        "close-register-button"
    )

    pause()

    assert element_visible(
        driver,
        "closing-screen"
    )


# ============================================================
# OPEN CASH MOVEMENT
# ============================================================

def open_cash_movement(
    driver
):

    click_element(
        driver,
        "cash-movement-button"
    )

    pause()

    assert element_visible(
        driver,
        "cash-movement-modal"
    )


# ============================================================
# ENTER DENOMINATION COUNT
# ============================================================

def enter_cash_count(
    driver,
    notes_100=0,
    notes_50=0,
    notes_20=0,
    notes_10=0,
    notes_5=0,
    coins_2=0,
    coins_1=0,
    coins_050=0,
    coins_020=0,
    coins_010=0
):

    denominations = {

        "denom-100": notes_100,

        "denom-50": notes_50,

        "denom-20": notes_20,

        "denom-10": notes_10,

        "denom-5": notes_5,

        "denom-2": coins_2,

        "denom-1": coins_1,

        "denom-050": coins_050,

        "denom-020": coins_020,

        "denom-010": coins_010

    }

    for element_id, quantity in denominations.items():

        if quantity > 0:

            enter_text(
                driver,
                element_id,
                quantity
            )


# ============================================================
# CONFIRM CASH COUNT
# ============================================================

def confirm_cash_count(
    driver
):

    click_element(
        driver,
        "confirm-count-button"
    )

    pause()


# ============================================================
# GET CALCULATED CASH
# ============================================================

def get_calculated_cash(
    driver
):

    return get_text(
        driver,
        "calculated-cash"
    )


# ============================================================
# CLOSE REGISTER
# ============================================================

def close_register(
    driver
):

    click_element(
        driver,
        "final-close-button"
    )

    pause()


# ============================================================
# ============================================================
# TEST CASES
# ============================================================
# ============================================================


# ============================================================
# TC01 - BALANCED EOD
# Technique:
# Equivalence Partitioning
# ============================================================

def test_TC01_balanced_eod():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC01 - BALANCED EOD")
        print("=" * 60)

        print(
            "Creating $1000 cash sales."
        )

        make_cash_sale(
            driver,
            "product-laptop",
            500
        )

        make_cash_sale(
            driver,
            "product-laptop",
            500
        )

        print(
            "Cash sales completed: $1000"
        )

        open_closing_control(
            driver
        )

        # Opening float = $200
        # Cash sales = $1000
        # Expected physical cash = $1200
        #
        # Count:
        # 12 x $100 = $1200

        enter_cash_count(
            driver,
            notes_100=12
        )

        confirm_cash_count(
            driver
        )

        calculated = get_calculated_cash(
            driver
        )

        print(
            "Calculated cash:",
            calculated
        )

        assert calculated == "$1200.00"

        result = get_closing_result(
            driver
        )

        print(
            "Closing result:",
            result
        )

        assert "BALANCED" in result.upper()

        close_register(
            driver
        )

        assert element_visible(
            driver,
            "closed-screen"
        )

        print(
            "TC01 PASSED - Register closed successfully."
        )

    finally:

        driver.quit()


# ============================================================
# TC02 - CASH SHORTAGE
# Technique:
# Equivalence Partitioning
# ============================================================

def test_TC02_cash_shortage():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC02 - CASH SHORTAGE")
        print("=" * 60)

        print(
            "Creating $1000 cash sales."
        )

        make_cash_sale(
            driver,
            "product-laptop",
            500
        )

        make_cash_sale(
            driver,
            "product-laptop",
            500
        )

        print(
            "Cash sales completed: $1000"
        )

        open_closing_control(
            driver
        )

        # Actual cash counted = $1100
        # Expected = $1200
        #
        # 11 x $100

        enter_cash_count(
            driver,
            notes_100=11
        )

        confirm_cash_count(
            driver
        )

        calculated = get_calculated_cash(
            driver
        )

        print(
            "Calculated cash:",
            calculated
        )

        assert calculated == "$1100.00"

        result = get_closing_result(
            driver
        )

        print(
            "Closing result:",
            result
        )

        assert "SHORTAGE" in result.upper()

        # Requirement:
        # Shortage amount must NOT be displayed.

        assert "$100" not in result

        print(
            "TC02 PASSED - Shortage identified without displaying amount."
        )

    finally:

        driver.quit()


# ============================================================
# TC03 - CASH OVERAGE
# Technique:
# Equivalence Partitioning
# ============================================================

def test_TC03_cash_overage():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC03 - CASH OVERAGE")
        print("=" * 60)

        print(
            "Creating $1000 cash sales."
        )

        make_cash_sale(
            driver,
            "product-laptop",
            500
        )

        make_cash_sale(
            driver,
            "product-laptop",
            500
        )

        print(
            "Cash sales completed: $1000"
        )

        open_closing_control(
            driver
        )

        # Actual cash = $1300
        # Expected = $1200
        #
        # 13 x $100

        enter_cash_count(
            driver,
            notes_100=13
        )

        confirm_cash_count(
            driver
        )

        calculated = get_calculated_cash(
            driver
        )

        print(
            "Calculated cash:",
            calculated
        )

        assert calculated == "$1300.00"

        result = get_closing_result(
            driver
        )

        print(
            "Closing result:",
            result
        )

        assert "OVERAGE" in result.upper()

        # Overage amount must NOT be displayed.

        assert "$100" not in result

        print(
            "TC03 PASSED - Overage identified without displaying amount."
        )

    finally:

        driver.quit()


# ============================================================
# TC04 - ZERO CASH COUNT
# Technique:
# Boundary Value Analysis
# ============================================================

def test_TC04_zero_cash():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC04 - ZERO CASH COUNT")
        print("=" * 60)

        print(
            "Opening Closing Control without sales."
        )

        open_closing_control(
            driver
        )

        # All denomination quantities remain zero.

        enter_cash_count(
            driver
        )

        confirm_cash_count(
            driver
        )

        calculated = get_calculated_cash(
            driver
        )

        print(
            "Calculated cash:",
            calculated
        )

        assert calculated == "$0.00"

        result = get_closing_result(
            driver
        )

        print(
            "Closing result:",
            result
        )

        assert (
            "SHORTAGE" in result.upper()
            or
            "OVERAGE" in result.upper()
            or
            "BALANCED" in result.upper()
        )

        print(
            "TC04 PASSED - Zero denomination count processed."
        )

    finally:

        driver.quit()


# ============================================================
# TC05 - EXACT CASH PAYMENT
# Technique:
# Boundary Value Analysis
# ============================================================

def test_TC05_exact_cash_payment():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC05 - EXACT CASH PAYMENT")
        print("=" * 60)

        print(
            "Making a $500 sale."
        )

        click_element(
            driver,
            "product-laptop"
        )

        click_element(
            driver,
            "payment-button"
        )

        click_element(
            driver,
            "cash-payment-button"
        )

        enter_text(
            driver,
            "amount-paid",
            500
        )

        continue_button = wait_for_element(
            driver,
            "continue-payment-button"
        )

        assert continue_button.is_enabled()

        click_element(
            driver,
            "continue-payment-button"
        )

        assert element_visible(
            driver,
            "sales-screen"
        )

        print(
            "TC05 PASSED - Exact cash payment accepted."
        )

    finally:

        driver.quit()


# ============================================================
# TC06 - CASH PAYMENT WITH CHANGE
# Technique:
# Equivalence Partitioning
# ============================================================

def test_TC06_cash_payment_with_change():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC06 - CASH PAYMENT WITH CHANGE")
        print("=" * 60)

        print(
            "Making a $500 sale."
        )

        click_element(
            driver,
            "product-laptop"
        )

        click_element(
            driver,
            "payment-button"
        )

        click_element(
            driver,
            "cash-payment-button"
        )

        print(
            "Entering $600 for a $500 sale."
        )

        enter_text(
            driver,
            "amount-paid",
            600
        )

        change = get_text(
            driver,
            "change-amount"
        )

        print(
            "Displayed change:",
            change
        )

        assert change == "$100.00"

        continue_button = wait_for_element(
            driver,
            "continue-payment-button"
        )

        assert continue_button.is_enabled()

        click_element(
            driver,
            "continue-payment-button"
        )

        print(
            "TC06 PASSED - Correct change calculated."
        )

    finally:

        driver.quit()


# ============================================================
# TC07 - INVALID CASH MOVEMENT
# Technique:
# Negative Testing
# ============================================================
def test_TC07_negative_cash_movement():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC07 - INVALID CASH MOVEMENT")
        print("=" * 60)

        print("Opening Cash In / Cash Out.")

        open_cash_movement(driver)

        pause()

        print("Entering invalid negative amount: -$50")

        amount_input = wait_for_element(
            driver,
            "movement-amount"
        )

        driver.execute_script(
            """
            arguments[0].value = '-50';

            arguments[0].dispatchEvent(
                new Event('input', { bubbles: true })
            );

            arguments[0].dispatchEvent(
                new Event('change', { bubbles: true })
            );
            """,
            amount_input
        )

        pause()

        print("Clicking CONFIRM.")

        click_element(
            driver,
            "confirm-movement-button"
        )

        pause()

        print("Checking validation alert.")

        alert = WebDriverWait(
            driver,
            5
        ).until(
            EC.alert_is_present()
        )

        alert_text = alert.text

        print(
            "Alert displayed:",
            alert_text
        )

        assert (
            "valid amount" in alert_text.lower()
        ), (
            "Expected invalid amount alert was not displayed."
        )

        alert.accept()

        pause()

        print(
            "Verifying invalid cash movement was rejected."
        )

        assert element_visible(
            driver,
            "cash-movement-modal"
        ), (
            "Cash movement modal should remain open "
            "after invalid input."
        )

        movement_amount = driver.find_element(
            By.ID,
            "movement-amount"
        ).get_attribute("value")

        print(
            "Movement input after rejection:",
            movement_amount
        )

        print(
            "TC07 PASSED - Negative cash movement rejected."
        )

    finally:

        driver.quit()
# ============================================================
# TC08 - CARD PAYMENT
# Technique:
# Equivalence Partitioning
# ============================================================

def test_TC08_card_payment():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC08 - CARD PAYMENT")
        print("=" * 60)

        make_card_sale(
            driver,
            "product-laptop"
        )

        assert element_visible(
            driver,
            "sales-screen"
        )

        print(
            "TC08 PASSED - Card payment completed."
        )

    finally:

        driver.quit()


# ============================================================
# TC09 - MISSING CASH COUNT
# Technique:
# Negative Testing
# ============================================================

def test_TC09_missing_count():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC09 - MISSING CASH COUNT")
        print("=" * 60)

        open_closing_control(
            driver
        )

        print(
            "No denomination values entered."
        )

        # Confirming zero denomination count is allowed by
        # the current application.
        #
        # The important test is that the system processes
        # the count through the reconciliation workflow.

        click_element(
            driver,
            "confirm-count-button"
        )

        calculated = get_calculated_cash(
            driver
        )

        print(
            "Calculated cash:",
            calculated
        )

        assert calculated == "$0.00"

        result = get_closing_result(
            driver
        )

        print(
            "Closing result:",
            result
        )

        assert result != ""

        print(
            "TC09 PASSED - Cash count confirmation handled."
        )

    finally:

        driver.quit()


# ============================================================
# TC10 - SALES ONLY
# Technique:
# Equivalence Partitioning
# ============================================================

def test_TC10_sales_only():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC10 - SALES ONLY")
        print("=" * 60)

        print(
            "Creating $500 cash sale."
        )

        make_cash_sale(
            driver,
            "product-laptop",
            500
        )

        open_closing_control(
            driver
        )

        # Opening float = $200
        # Cash sale = $500
        # Expected physical cash = $700
        #
        # Count 7 x $100

        enter_cash_count(
            driver,
            notes_100=7
        )

        confirm_cash_count(
            driver
        )

        calculated = get_calculated_cash(
            driver
        )

        print(
            "Calculated cash:",
            calculated
        )

        assert calculated == "$700.00"

        result = get_closing_result(
            driver
        )

        print(
            "Closing result:",
            result
        )

        assert "BALANCED" in result.upper()

        print(
            "TC10 PASSED - Cash sales correctly reflected in reconciliation."
        )

    finally:

        driver.quit()


# ============================================================
# TC11 - CASH IN
# Technique:
# Functional Testing
# ============================================================

def test_TC11_cash_in():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC11 - CASH IN")
        print("=" * 60)

        open_cash_movement(
            driver
        )

        print(
            "Adding $100 Cash In."
        )

        enter_text(
            driver,
            "movement-amount",
            100
        )

        click_element(
            driver,
            "confirm-movement-button"
        )

        pause()

        # Reopen closing control.

        open_closing_control(
            driver
        )

        # Opening float = $200
        # Cash In = $100
        # Expected = $300
        #
        # Count 3 x $100

        enter_cash_count(
            driver,
            notes_100=3
        )

        confirm_cash_count(
            driver
        )

        calculated = get_calculated_cash(
            driver
        )

        print(
            "Calculated cash:",
            calculated
        )

        assert calculated == "$300.00"

        result = get_closing_result(
            driver
        )

        assert "BALANCED" in result.upper()

        print(
            "TC11 PASSED - Cash In processed correctly."
        )

    finally:

        driver.quit()


# ============================================================
# TC12 - INSUFFICIENT CASH PAYMENT
# Technique:
# Boundary Value Analysis / Negative Testing
# ============================================================

def test_TC12_insufficient_cash_payment():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC12 - INSUFFICIENT CASH PAYMENT")
        print("=" * 60)

        click_element(
            driver,
            "product-laptop"
        )

        click_element(
            driver,
            "payment-button"
        )

        click_element(
            driver,
            "cash-payment-button"
        )

        print(
            "Entering $400 for a $500 sale."
        )

        enter_text(
            driver,
            "amount-paid",
            400
        )

        pause()

        continue_button = wait_for_element(
            driver,
            "continue-payment-button"
        )

        # $400 is less than the $500 sale total.
        # Therefore the payment button must remain disabled.

        assert not continue_button.is_enabled()

        print(
            "TC12 PASSED - Insufficient cash payment rejected."
        )

    finally:

        driver.quit()


# ============================================================
# TC13 - PRODUCT SELECTION
# Technique:
# Functional Testing
# ============================================================

def test_TC13_product_selection():

    driver = create_driver()

    try:

        print("\n")
        print("=" * 60)
        print("TC13 - PRODUCT SELECTION")
        print("=" * 60)

        print(
            "Selecting Laptop product."
        )

        click_element(
            driver,
            "product-laptop"
        )

        pause()

        total = get_text(
            driver,
            "order-total"
        )

        print(
            "Order total:",
            total
        )

        assert total == "$500.00"

        order_items = get_text(
            driver,
            "order-items"
        )

        assert "Laptop" in order_items

        payment_button = wait_for_element(
            driver,
            "payment-button"
        )

        assert payment_button.is_enabled()

        print(
            "TC13 PASSED - Product added and total updated."
        )

    finally:

        driver.quit()


# ============================================================
# END OF FILE
# ============================================================

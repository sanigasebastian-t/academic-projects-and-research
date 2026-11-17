// ============================================================
// EOD POS DEMO
// JavaScript Application Logic
//
// Feature:
// End-of-Day Cash Reconciliation
//
// Important behaviour:
// 1. Expected cash is NOT displayed to the user.
// 2. Cashier counts physical notes/coins.
// 3. System calculates counted cash internally.
// 4. Discrepancy is NOT displayed before confirmation.
// 5. After confirmation, only BALANCED / SHORTAGE / OVERAGE
//    is displayed.
// 6. Shortage/overage amount is NOT displayed.
// ============================================================



// ============================================================
// SESSION DATA
// ============================================================

let openingFloat = 200.00;

let cashSales = 0.00;

let cashIn = 0.00;

let cashOut = 0.00;

let expectedCash = 200.00;

let currentSaleTotal = 0.00;

let selectedPaymentMethod = "";

let sessionOpen = true;

let cashCountConfirmed = false;



// ============================================================
// PAGE LOAD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log("EOD POS Demo loaded.");

        updateExpectedCash();

        setupProductButtons();

        setupPaymentButtons();

        setupCashMovement();

        setupClosingControls();

        setupDenominationInputs();

    }
);



// ============================================================
// PRODUCT / SALES
// ============================================================

function setupProductButtons() {

    const products =
        document.querySelectorAll(".product");


    products.forEach(
        function (product) {

            product.addEventListener(
                "click",
                function () {

                    if (!sessionOpen) {
                        return;
                    }


                    const price =
                        parseFloat(
                            product.dataset.price
                        );


                    const name =
                        product.dataset.name;


                    addProductToOrder(
                        name,
                        price
                    );

                }
            );

        }
    );

}



// ============================================================
// ADD PRODUCT TO ORDER
// ============================================================

function addProductToOrder(
    name,
    price
) {

    currentSaleTotal += price;


    const orderItems =
        document.getElementById(
            "order-items"
        );


    const emptyOrder =
        document.getElementById(
            "empty-order"
        );


    if (emptyOrder) {

        emptyOrder.remove();

    }


    const item =
        document.createElement(
            "div"
        );


    item.className =
        "order-item";


    item.innerHTML =
        `
        <span>${name}</span>
        <strong>$${price.toFixed(2)}</strong>
        `;


    orderItems.appendChild(item);


    updateSalesDisplay();

    enablePaymentButton();

}



// ============================================================
// UPDATE CURRENT SALE
// ============================================================

function updateSalesDisplay() {

    const total =
        document.getElementById(
            "order-total"
        );


    if (total) {

        total.textContent =
            "$" +
            currentSaleTotal.toFixed(2);

    }

}



// ============================================================
// ENABLE PAYMENT BUTTON
// ============================================================

function enablePaymentButton() {

    const paymentButton =
        document.getElementById(
            "payment-button"
        );


    if (paymentButton) {

        paymentButton.disabled =
            currentSaleTotal <= 0;

    }

}



// ============================================================
// PAYMENT BUTTONS
// ============================================================

function setupPaymentButtons() {

    const paymentButton =
        document.getElementById(
            "payment-button"
        );


    if (paymentButton) {

        paymentButton.addEventListener(
            "click",
            function () {

                openPaymentScreen();

            }
        );

    }


    const cashButton =
        document.getElementById(
            "cash-payment-button"
        );


    if (cashButton) {

        cashButton.addEventListener(
            "click",
            function () {

                selectCashPayment();

            }
        );

    }


    const cardButton =
        document.getElementById(
            "card-payment-button"
        );


    if (cardButton) {

        cardButton.addEventListener(
            "click",
            function () {

                selectCardPayment();

            }
        );

    }


    const amountPaid =
        document.getElementById(
            "amount-paid"
        );


    if (amountPaid) {

        amountPaid.addEventListener(
            "input",
            function () {

                calculateChange();

            }
        );

    }


    const continueCashButton =
        document.getElementById(
            "continue-payment-button"
        );


    if (continueCashButton) {

        continueCashButton.addEventListener(
            "click",
            function () {

                completeCashPayment();

            }
        );

    }


    const continueCardButton =
        document.getElementById(
            "continue-card-payment-button"
        );


    if (continueCardButton) {

        continueCardButton.addEventListener(
            "click",
            function () {

                completeCardPayment();

            }
        );

    }

}



// ============================================================
// OPEN PAYMENT SCREEN
// ============================================================

function openPaymentScreen() {

    hideScreen("sales-screen");

    showScreen("payment-screen");


    const paymentTotal =
        document.getElementById(
            "payment-total"
        );


    paymentTotal.textContent =
        "$" +
        currentSaleTotal.toFixed(2);

}



// ============================================================
// SELECT CASH PAYMENT
// ============================================================

function selectCashPayment() {

    selectedPaymentMethod =
        "cash";


    showScreen(
        "cash-payment-section"
    );


    hideScreen(
        "card-payment-section"
    );


    const amountPaid =
        document.getElementById(
            "amount-paid"
        );


    amountPaid.value = "";

    amountPaid.focus();


    const continueButton =
        document.getElementById(
            "continue-payment-button"
        );


    continueButton.disabled =
        true;

}



// ============================================================
// SELECT CARD PAYMENT
// ============================================================

function selectCardPayment() {

    selectedPaymentMethod =
        "card";


    hideScreen(
        "cash-payment-section"
    );


    showScreen(
        "card-payment-section"
    );

}



// ============================================================
// CALCULATE CHANGE
// ============================================================

function calculateChange() {

    const amountPaidInput =
        document.getElementById(
            "amount-paid"
        );


    const continueButton =
        document.getElementById(
            "continue-payment-button"
        );


    const changeDisplay =
        document.getElementById(
            "change-amount"
        );


    const amountPaid =
        parseFloat(
            amountPaidInput.value
        );


    if (
        isNaN(amountPaid) ||
        amountPaid < currentSaleTotal
    ) {

        changeDisplay.textContent =
            "$0.00";


        continueButton.disabled =
            true;


        return;

    }


    const change =
        amountPaid -
        currentSaleTotal;


    changeDisplay.textContent =
        "$" +
        change.toFixed(2);


    continueButton.disabled =
        false;

}



// ============================================================
// COMPLETE CASH PAYMENT
// ============================================================

function completeCashPayment() {

    const amountPaidInput =
        document.getElementById(
            "amount-paid"
        );


    const amountPaid =
        parseFloat(
            amountPaidInput.value
        );


    if (
        isNaN(amountPaid) ||
        amountPaid < currentSaleTotal
    ) {

        alert(
            "Please enter a valid amount paid."
        );


        return;

    }


    // Only the sale value is added to cash sales.
    // Customer change is not counted as a sale.
    cashSales += currentSaleTotal;


    updateExpectedCash();


    finishSale();

}



// ============================================================
// COMPLETE CARD PAYMENT
// ============================================================

function completeCardPayment() {

    // Card sales do not increase physical cash.
    finishSale();

}



// ============================================================
// FINISH SALE
// ============================================================

function finishSale() {

    currentSaleTotal =
        0.00;


    selectedPaymentMethod =
        "";


    updateSalesDisplay();


    const orderItems =
        document.getElementById(
            "order-items"
        );


    orderItems.innerHTML =
        `
        <p id="empty-order">
            No products added.
        </p>
        `;


    enablePaymentButton();


    hideScreen(
        "payment-screen"
    );


    showScreen(
        "sales-screen"
    );


    updateExpectedCash();

}



// ============================================================
// CASH MOVEMENT
// ============================================================

function setupCashMovement() {

    const movementButton =
        document.getElementById(
            "cash-movement-button"
        );


    movementButton.addEventListener(
        "click",
        function () {

            openCashMovement();

        }
    );


    const confirmButton =
        document.getElementById(
            "confirm-movement-button"
        );


    confirmButton.addEventListener(
        "click",
        function () {

            confirmCashMovement();

        }
    );


    const cancelButton =
        document.getElementById(
            "cancel-movement-button"
        );


    cancelButton.addEventListener(
        "click",
        function () {

            closeCashMovement();

        }
    );

}



// ============================================================
// OPEN CASH MOVEMENT
// ============================================================

function openCashMovement() {

    showScreen(
        "cash-movement-modal"
    );

}



// ============================================================
// CLOSE CASH MOVEMENT
// ============================================================

function closeCashMovement() {

    hideScreen(
        "cash-movement-modal"
    );


    document.getElementById(
        "movement-amount"
    ).value = "";

}



// ============================================================
// CONFIRM CASH MOVEMENT
// ============================================================

function confirmCashMovement() {

    const type =
        document.getElementById(
            "movement-type"
        ).value;


    const amountInput =
        document.getElementById(
            "movement-amount"
        );


    const amount =
        parseFloat(
            amountInput.value
        );


    if (
        isNaN(amount) ||
        amount <= 0
    ) {

        alert(
            "Please enter a valid amount."
        );


        return;

    }


    if (type === "in") {

        cashIn += amount;

    }

    else {

        cashOut += amount;

    }


    updateExpectedCash();

    closeCashMovement();

}



// ============================================================
// UPDATE EXPECTED CASH
// ============================================================

function updateExpectedCash() {

    expectedCash =
        openingFloat +
        cashSales +
        cashIn -
        cashOut;


    console.log(
        "Expected cash calculated internally: $" +
        expectedCash.toFixed(2)
    );

}



// ============================================================
// CLOSE REGISTER BUTTON
// ============================================================

function setupClosingControls() {

    const closeRegisterButton =
        document.getElementById(
            "close-register-button"
        );


    closeRegisterButton.addEventListener(
        "click",
        function () {

            openClosingScreen();

        }
    );


    const confirmCountButton =
        document.getElementById(
            "confirm-count-button"
        );


    confirmCountButton.addEventListener(
        "click",
        function () {

            confirmCashCount();

        }
    );


    const finalCloseButton =
        document.getElementById(
            "final-close-button"
        );


    finalCloseButton.addEventListener(
        "click",
        function () {

            closeRegister();

        }
    );


    const cancelClosingButton =
        document.getElementById(
            "cancel-closing-button"
        );


    cancelClosingButton.addEventListener(
        "click",
        function () {

            cancelClosing();

        }
    );

}



// ============================================================
// OPEN CLOSING SCREEN
// ============================================================

function openClosingScreen() {

    if (!sessionOpen) {
        return;
    }


    hideScreen(
        "sales-screen"
    );


    showScreen(
        "closing-screen"
    );


    resetCashCount();


    console.log(
        "Closing Control opened."
    );

}



// ============================================================
// DENOMINATION INPUTS
// ============================================================

function setupDenominationInputs() {

    const inputs =
        document.querySelectorAll(
            ".denomination-input"
        );


    inputs.forEach(
        function (input) {

            input.addEventListener(
                "input",
                function () {

                    cashCountConfirmed =
                        false;


                    clearClosingResult();


                    hideScreen(
                        "counted-cash-display"
                    );


                    const finalCloseButton =
                        document.getElementById(
                            "final-close-button"
                        );


                    finalCloseButton.disabled =
                        true;

                }
            );


            input.addEventListener(
                "change",
                function () {

                    if (
                        parseFloat(input.value) < 0
                    ) {

                        input.value = "0";

                    }

                }
            );

        }
    );

}



// ============================================================
// CALCULATE PHYSICAL CASH
// ============================================================

function calculatePhysicalCash() {

    const inputs =
        document.querySelectorAll(
            ".denomination-input"
        );


    let totalCents = 0;


    inputs.forEach(
        function (input) {

            let quantity =
                parseInt(
                    input.value,
                    10
                );


            if (
                isNaN(quantity) ||
                quantity < 0
            ) {

                quantity = 0;

            }


            const denomination =
                parseFloat(
                    input.dataset.value
                );


            const denominationCents =
                Math.round(
                    denomination * 100
                );


            totalCents +=
                quantity *
                denominationCents;

        }
    );


    return totalCents / 100;

}



// ============================================================
// CONFIRM CASH COUNT
// ============================================================

function confirmCashCount() {

    const inputs =
        document.querySelectorAll(
            ".denomination-input"
        );


    let hasInvalidInput =
        false;


    inputs.forEach(
        function (input) {

            const value =
                input.value.trim();


            if (value !== "") {

                const quantity =
                    Number(value);


                if (
                    !Number.isInteger(quantity) ||
                    quantity < 0
                ) {

                    hasInvalidInput =
                        true;

                }

            }

        }
    );


    if (hasInvalidInput) {

        showClosingResult(
            "INVALID CASH COUNT",
            "error"
        );


        return;

    }


    const countedCash =
        calculatePhysicalCash();


    const calculatedCashElement =
        document.getElementById(
            "calculated-cash"
        );


    calculatedCashElement.textContent =
        "$" +
        countedCash.toFixed(2);


    showScreen(
        "counted-cash-display"
    );


    cashCountConfirmed =
        true;


    const difference =
        Math.round(
            (
                countedCash -
                expectedCash
            ) * 100
        ) / 100;


    // ========================================================
    // IMPORTANT:
    // Discrepancy is shown ONLY AFTER confirmation.
    //
    // The amount is deliberately NOT shown.
    // ========================================================

    if (difference === 0) {

        showClosingResult(
            "BALANCED",
            "success"
        );


        document.getElementById(
            "final-close-button"
        ).disabled = false;

    }

    else if (difference < 0) {

        showClosingResult(
            "CASH SHORTAGE",
            "warning"
        );


        document.getElementById(
            "final-close-button"
        ).disabled = true;

    }

    else {

        showClosingResult(
            "CASH OVERAGE",
            "warning"
        );


        document.getElementById(
            "final-close-button"
        ).disabled = true;

    }

}



// ============================================================
// FINAL REGISTER CLOSURE
// ============================================================

function closeRegister() {

    if (!cashCountConfirmed) {

        showClosingResult(
            "PLEASE CONFIRM THE CASH COUNT FIRST",
            "error"
        );


        return;

    }


    const countedCash =
        calculatePhysicalCash();


    const difference =
        Math.round(
            (
                countedCash -
                expectedCash
            ) * 100
        ) / 100;


    // Register can only close when balanced.
    if (difference !== 0) {

        showClosingResult(
            difference < 0
                ? "CASH SHORTAGE"
                : "CASH OVERAGE",
            "warning"
        );


        return;

    }


    sessionOpen =
        false;


    hideScreen(
        "closing-screen"
    );


    showScreen(
        "closed-screen"
    );


    const sessionStatus =
        document.getElementById(
            "session-status"
        );


    sessionStatus.textContent =
        "CLOSED";


    sessionStatus.classList.remove(
        "open"
    );


    sessionStatus.classList.add(
        "closed"
    );


    console.log(
        "Register successfully closed."
    );

}



// ============================================================
// CANCEL CLOSING
// ============================================================

function cancelClosing() {

    hideScreen(
        "closing-screen"
    );


    showScreen(
        "sales-screen"
    );


    resetCashCount();


    console.log(
        "Closing cancelled. Register remains open."
    );

}



// ============================================================
// RESET CASH COUNT
// ============================================================

function resetCashCount() {

    const inputs =
        document.querySelectorAll(
            ".denomination-input"
        );


    inputs.forEach(
        function (input) {

            input.value = "";

        }
    );


    cashCountConfirmed =
        false;


    hideScreen(
        "counted-cash-display"
    );


    document.getElementById(
        "calculated-cash"
    ).textContent =
        "$0.00";


    document.getElementById(
        "final-close-button"
    ).disabled =
        true;


    clearClosingResult();

}



// ============================================================
// SHOW CLOSING RESULT
// ============================================================

function showClosingResult(
    message,
    type
) {

    const result =
        document.getElementById(
            "closing-result"
        );


    result.textContent =
        message;


    result.className =
        "closing-result " +
        type;

}



// ============================================================
// CLEAR CLOSING RESULT
// ============================================================

function clearClosingResult() {

    const result =
        document.getElementById(
            "closing-result"
        );


    result.textContent =
        "";


    result.className =
        "closing-result";

}



// ============================================================
// SHOW SCREEN
// ============================================================

function showScreen(id) {

    const element =
        document.getElementById(id);


    if (!element) {
        return;
    }


    element.classList.remove(
        "hidden"
    );


    element.style.display =
        "block";

}



// ============================================================
// HIDE SCREEN
// ============================================================

function hideScreen(id) {

    const element =
        document.getElementById(id);


    if (!element) {
        return;
    }


    element.classList.add(
        "hidden"
    );


    element.style.display =
        "none";

}
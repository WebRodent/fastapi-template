document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('orderForm');

    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const productName = document.getElementById('productName').value;
        const quantity = document.getElementById('quantity').value;

        // Here you can handle the order data, for example, send it to a server
        alert(`Order placed for ${quantity} units of ${productName}.`);

        // Optionally, reset the form after submission
        form.reset();
    });
});

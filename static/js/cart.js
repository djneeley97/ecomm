var updateBtns = document.getElementsByClassName('update-cart')


for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function (e) {
        e.preventDefault();
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action', action)

        const userId = document.getElementById("hdnUserId").value;

        console.log('USER:', userId)
        if (userId == '0') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action, userId)
        }
    })
}



function addCookieItem(productId, action) {
    console.log('Not logged in')

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }
        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('remove item')
            delete cart[productId]
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    //location.reload()
}

function updateUserOrder(productId, action, userId) {
    console.log('User is authenticated, sending data...')

    var url = '/update_item/';

    const payload = {
        'productId': productId,
        'action': action,
        'userId': userId
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Data:', data)
        })
}
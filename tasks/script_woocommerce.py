from woocommerce import API

def ejecutar_script():
    wcapi = API(
        url="https://2d.com.co",
        consumer_key="ck_71bde58c9c399a383de844454801252067515028",
        consumer_secret="cs_59b05e7b0e065e72676dbab68765b375d81d15fb",
        version="wc/v3"
    )

    try:
        response = wcapi.get("orders", params={"per_page": 1, "order": "desc", "orderby": "date"})
        response.raise_for_status()

        orders = response.json()
        if orders:
            last_order = orders[0]
            customer_id = last_order.get('customer_id')
            billing_info = last_order.get('billing')
            shipping_info = last_order.get('shipping')

            result = f"ID de la última orden: {last_order['id']}\n"
            result += f"ID del cliente: {customer_id}\n"
            result += f"Nombre del cliente: {billing_info['first_name']} {billing_info['last_name']}\n"
            result += f"Correo electrónico: {billing_info['email']}\n"
            return result
        else:
            return "No se encontraron órdenes."
    except Exception as e:
        return f"Se produjo un error al obtener las órdenes: {e}"

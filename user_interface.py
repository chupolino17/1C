import main

while True:
    print("\n\nВыберите активность: "
        "\n\t1. Создать новый заказ"
        "\n\t2. Получить краткую информацию по заказу"
        "\n\t3. Получить полную информацию по заказу"
        "\n\t4. Изменить нформацию по заказу")
    choosen_action = int(input())
    if choosen_action == 1:
        print("Напишите информацию по заказу в следующем порядке:"
              "\n\t Фамилия"
              "\n\t Имя"
              "\n\t Отчество"
              "\n\t Адрес доставки"
              "\n\t Телефон для связи"
              "\n\t Дополнительная контактная информация"
              "\n\t Статус заказа"
              "\n\t Сумма к оплате"
              "\n(писать нужно в новых строчках)"
              )
        first_name = input().strip()
        second_name = input().strip()
        third_name = input().strip()
        address = input().strip()
        phone_number = input().strip()
        contacts = input().strip()
        status = input().strip()
        sum = int(input().strip())
        main.create_order(status,
                     sum,
                     first_name,
                     second_name,
                     third_name,
                     address,
                     contacts,
                     phone_number)
    elif choosen_action == 2:
        print("\n\tВведите номер заказа")
        order_id = int(input())
        try:
            order_info = main.get_order_info(order_id)
            print("Найденная информацию по заказу:" + \
                "\n\t Статус заказа: " + str(order_info[2]) + \
                "\n\t Сумма к оплате: " + str(order_info[3]) + \
                "\n\t Дата создания: " + str(order_info[4].strftime("%d-%m-%Y %H:%M:%S")) + \
                "\n\t Дата изменения: " + str(order_info[5].strftime("%d-%m-%Y %H:%M:%S"))
                )
        except:
            print('Такого заказа не существует, или повторите попытку позже')
    elif choosen_action == 3:
        print("\n\tВведите номер заказа")
        order_id = int(input())
        order_info = main.get_full_order_info(order_id)
        print(order_info)
        try:
            print("Найденная информацию по заказу:" + \
                  "\n\t Фамилия: " + str(order_info[7]) + \
                  "\n\t Имя: " + str(order_info[8]) + \
                  "\n\t Отчество: " + str(order_info[9]) + \
                  "\n\t Адрес доставки: " + str(order_info[10]) + \
                  "\n\t Телефон для связи: " + str(order_info[12]) + \
                  "\n\t Дополнительная контактная информация: " + str(order_info[11]) + \
                  "\n\t Статус заказа: " + str(order_info[2]) + \
                  "\n\t Сумма к оплате: " + str(order_info[3]) + \
                  "\n\t Дата создания: " + str(order_info[4].strftime("%d-%m-%Y %H:%M:%S")) + \
                  "\n\t Дата изменения: " + str(order_info[5].strftime("%d-%m-%Y %H:%M:%S"))
                  )
        except:
            print('Такого заказа не существует, или повторите попытку позже')
    elif choosen_action == 4:
        # Обращение к main.change_full_order_info
        # Не успеваю дописать
        continue
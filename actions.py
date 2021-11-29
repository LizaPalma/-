def BlockAcc(connection, client_id):
    while True:
        cur = connection.cursor()
        print('''Какие действия?
            1 Разблокировать кошелек
            2 Блокировать кошелек
            3 Назад
            ''')
        deystvie = int(input("\nВыберите действие: "))
        if deystvie == 1:
            cur.execute("UPDATE clients SET flag = ? WHERE client_id = ?", (0, client_id))
            connection.commit()
            print("Ваш кошелёк успешно разблокирован")
        elif deystvie == 2:
            cur.execute("UPDATE clients SET flag = ? WHERE client_id = ?", (1, client_id))
            connection.commit()
            print("Ваш кошелёк успешно заблокирован")
        elif deystvie == 3:
            break
        else:
            print('Неверная команда. Попробуйте еще раз')
            continue

def CheckBlock(connection, client_id):
    cur = connection.cursor()
    cur.execute("SELECT flag FROM clients WHERE client_id = ?", (client_id,))
    check_client_id = cur.fetchone()[0]
    if check_client_id == 0:
        return 0
    elif check_client_id == 1:
        return 1

def AddShet(connection, client_id):
    cur = connection.cursor()
    iso = 'RUB'
    while True:
        print('''Какой счет создать?
        1 В рублях
        2 Валютный
        3 Вернуться назад
        ''')
        x = int(input("Введите номер команды: "))
        if x == 1:
            shet_num = int(str(client_id) + '810')
            cur.execute("SELECT count(*) FROM sheta WHERE client_id = ? and shet_num = ?", (client_id, shet_num,)) # есть ли с таким айди и номером счета клиент
            check_client_id = cur.fetchone()[0]
            if check_client_id == 1:
                print('Счет уже существует. Операция невозможна')
            else:
                cur.execute("insert into sheta (client_id, shet_num, iso) values(?, ?, ?)", (client_id, shet_num, iso,))
                connection.commit()
                print('Ваш счет '+ str(shet_num) + ' создан.')
        elif x == 2:
            while True:
                code_iso = int(input("Введите код валюты: "))
                cur.execute("SELECT count(*) FROM rates WHERE cod_iso = ?", (code_iso,))
                check_iso = cur.fetchone()[0]
                if check_iso == 0:
                    print('Неверный код валюты. Попробуйте еще раз')
                else:
                    break

            shet_num = int(str(client_id) + str(code_iso))
            cur.execute("SELECT count(*) FROM sheta WHERE client_id = ? and shet_num = ?", (client_id, shet_num,))
            check_client_id = cur.fetchone()[0]
            if check_client_id == 1:
                print('Счет уже существует. Операция невозможна')
            else:
                cur.execute("SELECT iso FROM rates WHERE cod_iso = ?", (code_iso,))
                name_iso = cur.fetchone()[0]
                cur.execute("insert into sheta (client_id, shet_num, iso) values(?, ?, ?)", (client_id, shet_num, name_iso,))
                connection.commit()
                print('Ваш счет ' + str(shet_num) + ' создан.')
        elif x == 3:
            break
        else:
            print('Неверная команда. Попробуйте еще раз')
            continue

def ShowBalance(connection, client_id):
    cur = connection.cursor()
    cur.execute("SELECT * from sheta WHERE client_id = ?", (client_id,))
    clients = cur.fetchall()
    for client in clients:
        print(client)

def ShowAllBalance(connection):
    cur = connection.cursor()
    cur.execute("SELECT * from sheta")
    clients = cur.fetchall()
    for client in clients:
        print(client)

def AddBalance(connection, client_id, put_num_shet, value):
    cur = connection.cursor()
    cur.execute("SELECT balance from sheta WHERE shet_num = ?", (put_num_shet,))
    cur_balance = cur.fetchone()[0]
    new_balance = cur_balance + value
    cur.execute("UPDATE sheta SET balance = ? WHERE shet_num = ?", (new_balance, put_num_shet))
    cur.execute("INSERT into operation (client_id, type, description, shet_from, value) VALUES (?,?,?,?,?)", (client_id, 1, 'Пополнение', put_num_shet, value))
    connection.commit()
    print("Счет успешно пополнен на: " + str(value))
    cur.execute("SELECT balance from sheta WHERE shet_num = ?", (put_num_shet,))
    balance = cur.fetchone()[0]
    print("Текущий баланс = " + str(balance))

def MinusBalance(connection, client_id, put_num_shet, value):
    cur = connection.cursor()
    cur.execute("SELECT balance from sheta WHERE shet_num = ?", (put_num_shet,))
    cur_balance = cur.fetchone()[0]
    new_balance = cur_balance - value
    if new_balance < 0:
        return print('На счете недостаточно средств. Ваш баланс: ' + str(cur_balance))
    cur.execute("UPDATE sheta SET balance = ? WHERE shet_num = ?", (new_balance, put_num_shet))
    cur.execute("INSERT into operation (client_id, type, description, shet_from, value) VALUES (?,?,?,?,?)", (client_id, 2, 'Списание', put_num_shet, value))
    connection.commit()
    print("С Вашего счета снято: " + str(value))
    cur.execute("SELECT balance from sheta WHERE shet_num = ?", (put_num_shet,))
    balance = cur.fetchone()[0]
    print("Текущий баланс = " + str(balance))

def Transaction(connection, client_id, put_from_shet, put_to_shet, value):
    # def rateval(code):
    #     if code == 810:
    #         return 1
    #     else:
    #         cur = connection.cursor()
    #         cur.execute("SELECT rate from rates WHERE code_iso = ?", (code,))
    #         rate = cur.fetchone()[0]
    #         return rate
    #
    # ## Получаем код валюты
    # check_rub_from = put_from_shet[-3:]
    # check_rub_to = put_to_shet[-3:]
    #
    # # Получаем курс валюты
    # rate_from_bal = value * rateval(check_rub_from)
    # rate_to_bal = value * rateval(check_rub_to)
    cur = connection.cursor()
    cur.execute("SELECT balance from sheta WHERE shet_num = ?", (put_from_shet,))
    from_balance = cur.fetchone()[0]
    from_new_balance = from_balance - value
    if from_new_balance < 0:
        return print('На счете недостаточно средств. Ваш баланс: ' + str(from_balance))
####
    cur.execute("SELECT balance from sheta WHERE shet_num = ?", (put_to_shet,))
    to_balance = cur.fetchone()[0]
    new_to_balance = to_balance + value
#####
    cur.execute("UPDATE sheta SET balance = ? WHERE shet_num = ?", (from_new_balance, put_from_shet))
    cur.execute("UPDATE sheta SET balance = ? WHERE shet_num = ?", (new_to_balance, put_to_shet))
    cur.execute("INSERT into operation (client_id, type, description, shet_from, shet_to, value) VALUES (?,?,?,?,?,?)", (client_id, 3, 'Перевод', put_from_shet, put_to_shet, value))
    connection.commit()
    print("С Вашего счета снято: " + str(value))
    cur.execute("SELECT balance from sheta WHERE shet_num = ?", (put_from_shet,))
    balance = cur.fetchone()[0]
    print("Текущий баланс = " + str(balance))

def OperationHistory(connection, client_id):
    cur = connection.cursor()
    while True:
        print('''Выберите действие:
            1 Показать всю историю
            2 Показать только списания
            3 Показать только пополнения
            4 Показать только переводы
            5 Назад
            ''')
        x = int(input("Введите номер команды: "))
        if x == 1:
            cur.execute("SELECT * from operation WHERE client_id = ? order by op_date", (client_id,))
            operation = cur.fetchall()
            for op in operation:
                print(op)
        elif x == 2:
            cur.execute("SELECT * from operation WHERE client_id = ? and type = ? order by op_date", (client_id, 2))
            operation = cur.fetchall()
            for op in operation:
                print(op)
        elif x == 3:
            cur.execute("SELECT * from operation WHERE client_id = ? and type = ? order by op_date", (client_id, 1))
            operation = cur.fetchall()
            for op in operation:
                print(op)
        elif x == 4:
            cur.execute("SELECT * from operation WHERE client_id = ? and type = ? order by op_date", (client_id, 3))
            operation = cur.fetchall()
            for op in operation:
                print(op)
        elif x == 5:
            break
        else:
            print('Неверная команда. Попробуйте еще раз')
            continue
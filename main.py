import sqlite3
from actions import AddShet, ShowBalance, AddBalance, MinusBalance, Transaction, ShowAllBalance, CheckBlock, BlockAcc, OperationHistory
import csv



connection = sqlite3.connect('coshelek.db')

with open('ddl.sql', 'r') as sql_file:
    ddl = sql_file.read()
cur = connection.execute(ddl)
print('\nуспешно')
with open('shet.sql', 'r') as sql_file:
    ddl = sql_file.read()
cur = connection.execute(ddl)
print('\nуспешно')
with open('rates.sql', 'r') as sql_file:
    ddl = sql_file.read()
cur = connection.execute(ddl)
print('\nуспешно')
with open('operation.sql', 'r') as sql_file:
    ddl = sql_file.read()
cur = connection.execute(ddl)
print('\nуспешно')

cur.execute("SELECT * FROM rates")
check_rates = cur.fetchone()
if check_rates == None:
    a_file = open("cur.csv")
    rows = csv.reader(a_file, delimiter='\t')
    cur.executemany("INSERT INTO rates VALUES (?, ?, ?, ?, ?)", rows)
    cur.execute("SELECT * FROM rates")
    connection.commit()



owner_firstname = input("Привет, введите ваше имя: ").title()
owner_lastname = input("Введите фамилию: ").title()
owner_middlename = input("Введите отчество: ").title()
owner_city = input("Введите Ваш город: ").title()


add_client = connection.cursor()
add_client.execute("SELECT COUNT(*) FROM clients WHERE firstname = ? and lastname = ? and middlename = ? and city = ?", (owner_firstname, owner_lastname, owner_middlename, owner_city,))
rows = add_client.fetchone()[0]

if rows == 1:
    print('\nВы авторизованы')
else:
    add_client.execute('INSERT INTO clients (firstname, lastname, middlename, city) VALUES (?, ?, ?, ?)', (owner_firstname, owner_lastname, owner_middlename, owner_city,))
    connection.commit()
    print('Пользователь не найден. Создаем кошелек')
    print('Успешно создан кошелек пользователя: '+ owner_firstname + ' '+ owner_lastname + ' '+ owner_middlename + '.' ' ' 'Город: '+ owner_city)

add_client.execute('SELECT * FROM clients')
rows = add_client.fetchall()
for row in rows:
    print(row)

cur.execute("SELECT client_id FROM clients WHERE firstname = ? and lastname = ? and middlename = ? and city = ?",(owner_firstname, owner_lastname, owner_middlename, owner_city,))
client_id = cur.fetchone()[0] #узнаем какой у него айди
while True:
    print('''Какие действия?
    1 Создать расчетный счет
    2 Пополнить кошелек
    3 Списать деньги
    4 Перевести деньги
    5 Проверить баланс
    6 Блокировать/разблокировать кошелек
    7 Показать историю
    ''')
    x = int(input("Введите номер команды: "))
    flag = CheckBlock(connection, client_id) # заблокирован кошелек или нет
    if x == 1:
        if flag == 0:
            AddShet(connection, client_id)
        else:
            print("Ваш кошелёк заблокирован, Вам доступна только операция проверить баланс")
    elif x == 2:
        if flag == 0:
            CheckBlock(connection, client_id)
            ShowBalance(connection, client_id)
            put_num_shet = int(input("\nВведите номер счета: "))
            value = float(input("\nВведите сумму: "))
            AddBalance(connection,client_id, put_num_shet, value)
        else:
            print("Ваш кошелёк заблокирован, Вам доступна только операция проверить баланс")
    elif x == 3:
        if flag == 0:
            CheckBlock(connection, client_id)
            ShowBalance(connection, client_id)
            put_num_shet = int(input("\nВведите номер счета: "))
            value = float(input("\nВведите сумму: "))
            MinusBalance(connection, client_id, put_num_shet, value)
        else:
            print("Ваш кошелёк заблокирован, Вам доступна только операция проверить баланс")
    elif x == 4:
        if flag == 0:
            CheckBlock(connection, client_id)
            ShowBalance(connection, client_id)
            put_from_shet = int(input("\nВведите номер счета, с которого хотите списать: "))
            put_to_shet = int(input("\nВведите номер счета, на который хотите зачислить: "))
            value = float(input("\nВведите сумму: "))
            if put_from_shet == put_to_shet:
                print('Ошибка. Вы ввели свой счет')
            else:
                Transaction(connection, client_id, put_from_shet, put_to_shet, value)
        else:
            print("Ваш кошелёк заблокирован, Вам доступна только операция проверить баланс")
    elif x == 5:
        ShowBalance(connection, client_id)
    elif x == 6:
        BlockAcc(connection, client_id)
    elif x == 7:
        if flag == 0:
            CheckBlock(connection, client_id)
            OperationHistory(connection, client_id)
        else:
            print("Ваш кошелёк заблокирован, Вам доступна только операция проверить баланс")
    else:
        print('Неверная команда. Попробуйте еще раз')
        continue
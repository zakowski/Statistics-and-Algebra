import mysql.connector
from csv import reader
from mysql.connector import Error
import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt


# Przygotowanie odpowiedniej struktury bazy danych na wybrany temat - MySQL. (komis samochodowy)
# Skrypt ładujący dane do bazy - python z wykorzystaniem biblioteki łączącej się do bazy

def connect():
    user = str(input('Enter user login: '))
    password = str(input('Enter password: '))
    try:
        global connection
        connection = mysql.connector.connect(host="localhost",
                                             user=user,
                                             password=password,
                                             db='cars'
                                             )
        if connection.is_connected():
            print('Connected to MySQL database')
    except Error as e:
        print(e)


# Wprowadzenie danych do bazy z pliku csv
def insert_data():
    cursor = connection.cursor()
    with open('cars_data.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        if header is not None:
            for row in csv_reader:
                for i in csv_reader:
                    insert_data = "INSERT INTO cars_data(id, nazwa_auta, cena_auta, koszt_naprawy, czy_uszkodzony, kupcy, nr_vin, rok_produkcji) VALUES (%s, %s, %s, %s, %s, %s,%s, %s)"
                    value = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
                    cursor.execute(insert_data, value)
                    connection.commit()

    print('IT"S WORKS!')
    connection.close()


# Zapisywanie danych z bazy do pliku csv
def save_file():
    statement = 'SELECT * FROM cars_data'
    results = pd.read_sql_query(statement, connection)
    results = pd.DataFrame(results)
    results.to_csv("my_cars.csv", index=False)


# Statystki dla ceny posiadanych aut między rokiem 2010 - 2021
def value_by_date(start_prod, end_prod):
    cars = get_price_by_date(start_prod, end_prod)
    tmp = np.array(cars)
    price_max = max(cars)
    price_min = min(cars)
    mean = round(tmp.mean(), 2)
    std = round(tmp.std(), 2)
    median = statistics.median(tmp)
    median_low = statistics.median_low(tmp)
    r_pstdev = round(statistics.pstdev(tmp), 2)
    r_stdev = round(statistics.stdev(tmp), 2)

    print('max: ', price_max,
          ' min: ', price_min,
          ' mean: ', mean,
          ' std:', std,
          ' median: ', median,
          ' median_low: ', median_low,
          ' pstdev: ', r_pstdev,
          ' stdev: ', r_stdev)


def stats_for_col(tmp):
    col = np.array(tmp)
    print('max: ', np.max(col))
    print('min: ', np.min(col))
    print('mean: ', np.mean(col))
    print('std: ', np.std(col))
    print('median: ', statistics.median(col))
    print('median_low: ', statistics.median_low(col))
    print('result_pstdev: ', statistics.pstdev(col)) #odchylenie standardowe populacji
    print('result_stdev: ', statistics.stdev(col))
    print('variance: ', statistics.variance(col))


# Ceny aut miedzy rokiem X a Y
def get_price_by_date(start_prod, end_prod):
    cursor = connection.cursor()
    query = "SELECT cena_auta FROM cars_data WHERE rok_produkcji BETWEEN '{0}' AND '{1}';".format(
        start_prod,
        end_prod)
    cursor.execute(query)
    print(query)
    result = cursor.fetchall()
    query_result = [i[0] for i in result]
    cars = []
    for i in query_result:
        cars.append(i)
    return cars


# Zliczanie ile aut jakiej marki jest uszkodzonych
def cout_destroy_cars():
    cursor = connection.cursor()
    query = "SELECT nazwa_auta, COUNT(nazwa_auta) AS ilosc FROM cars_data WHERE czy_uszkodzony = 'true' GROUP BY nazwa_auta;"
    cursor.execute(query)
    print(query)
    result = cursor.fetchall()
    query_result = [i for i in result]
    cars = []
    for i in query_result:
        cars.append(i)
    return cars


# Zliczanie ile aut jakiej marki jest niewartych naprawy
def useless_car():
    cursor = connection.cursor()
    query = "SELECT nazwa_auta, COUNT(nazwa_auta) AS ilosc FROM cars_data WHERE cena_auta < koszt_naprawy GROUP BY nazwa_auta;"
    cursor.execute(query)
    print(query)
    result = cursor.fetchall()
    query_result = [i for i in result]
    cars = []
    for i in query_result:
        cars.append(i)
    return cars


# Ilosc aut niewartych naprawy i ilosc aut wartych naprawy
def efficient_car():
    cursor = connection.cursor()
    query1 = "SELECT COUNT(id) AS ilosc FROM cars_data WHERE cena_auta < koszt_naprawy;"
    cursor.execute(query1)
    print(query1)
    result = cursor.fetchall()

    query2 = "SELECT COUNT(id) AS ilosc FROM cars_data WHERE cena_auta > koszt_naprawy;"
    cursor.execute(query2)
    print(query2)
    result2 = cursor.fetchall()

    cars = [result[0][0], result2[0][0]]
    return cars


# Wstawianie nowych danych do nowych tabel do bazy
def insert_new_data():
    cursor = connection.cursor()
    query1 = "SELECT nazwa_auta, COUNT(nazwa_auta) AS warte FROM cars_data WHERE cena_auta > koszt_naprawy GROUP BY nazwa_auta;"
    cursor.execute(query1)
    result1 = cursor.fetchall()
    print(result1)
    query2 = "SELECT nazwa_auta, COUNT(nazwa_auta) AS niewarte FROM cars_data WHERE cena_auta < koszt_naprawy GROUP BY nazwa_auta;"
    cursor.execute(query2)
    result2 = cursor.fetchall()
    print(result2)
    for row in result1:
        for i in result1:
            in_data = "INSERT INTO efficient_car(nazwa_auta, warte) VALUES (%s, %s)"
            value = (i[0], i[1])
            cursor.execute(in_data, value)
            connection.commit()
    for row in result1:
        for i in result2:
            in_data = "INSERT INTO useless_car(nazwa_auta, niewarte) VALUES (%s, %s)"
            value = (i[0], i[1])
            cursor.execute(in_data, value)
            connection.commit()

    print('IT"S WORKS! - inserted data')
    connection.close()


def tests():
    cursor = connection.cursor()
    query = "SELECT koszt_naprawy FROM cars_data;"
    cursor.execute(query)
    print(query)
    result = cursor.fetchall()
    query_result = [i[0] for i in result]
    cars = []
    for i in query_result:
        cars.append(i)
    return cars

if __name__ == '__main__':
    connect()
    # insert_data()
    # save_file()
    start_prod = 2010
    end_prod = 2021
    print("get_price_by_date")
    total = get_price_by_date(start_prod, end_prod)
    print(total)
    print("\n")

    print("Statystyki dla col - ceny_aut - pomiedzy 2010 a 2021 rokiem")
    value_by_date(2010, 2021)
    print("\n")

    print("count_destroy_cars")
    destroyed = cout_destroy_cars()
    print(destroyed)
    print("\n")

    print("useless_car")
    car = useless_car()
    counter = [i[1] for i in car]
    name = [j[0] for j in car]

    # Auta niewarte naprawy
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    ax.pie(counter, labels=name, autopct='%1.2f%%')
    plt.show()

    print("\n")
    print("useless car and efficient_car")
    tab = efficient_car()
    print(tab)

    print("\n")
    #insert_new_data()

    print('Statystyki dla col - koszt_naprawy')
    stats_for_col(tests())

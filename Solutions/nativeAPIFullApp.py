"""
PURPOSE: Store stock data directly to InterSystems IRIS Data Platform using a custom structure
and generate trade data with methods from InterSystems IRIS
as well as call routine to print the version of InterSystems IRIS.

NOTES: When running,
1. Choose option 2 to store stock data natively.
2. Choose option 3 to retrieve stock data natively.
3. Choose option 4 to generate trades with random data using methods from InterSystems IRIS.
4. Choose option 5 to call InterSystems IRIS routine directly.
"""

from time import time
from random import randint
import irisnative


# Write to a test global
def set_test_global(iris_native):
    iris_native.set(8888, "^testglobal", "1")
    global_value = iris_native.get("^testglobal", "1")
    print("The value of ^testglobal(1) is {}".format(global_value))


# Store stock data directly into InterSystems IRIS
def store_stock_data(iris_native):
    # Clear global from previous runs
    iris_native.kill("^nyse")
    print("Storing stock data using Native API...")

    # Get stock data from file
    list_stock = []
    with open("all_stocks.csv") as f:
        lines = f.readlines()

        # Add stock data to list
        for line in lines:
            list_stock.append(line.rstrip("\n"))

    # Get current time
    start = int(time() * 1000)

    # Loop through list of stock and write global
    for i in range(1, len(list_stock)):
        iris_native.set(list_stock[i], "^nyse", i)

    # Get time consuming
    end = int(time() * 1000)
    time_consume = end - start
    print("Stored natively successfully. Execution time: {} ms".format(time_consume))


# Iterate over all nodes forwards and print
def print_nodes(iris_native):
    # Create an iterator
    subscript_iter = iris_native.iterator("^nyse")
    print("Iterating over all nodes forwards...")

    # Iterate over all nodes forwards
    for subscript, value in subscript_iter:
        print("subscript = {}, value = {}".format(subscript, value))


# Generate the list of trades
def generate_data(iris_native, object_count):
    # Loop through list of trade to generate data for each trade
    for _ in range(object_count):
        temp_date = "2018-01-01"
        temp_amount = iris_native.classMethodValue("%PopulateUtils", "Currency")
        temp_name = iris_native.classMethodValue("%PopulateUtils", "String") + \
                    iris_native.classMethodValue("%PopulateUtils", "String") + \
                    iris_native.classMethodValue("%PopulateUtils", "String")
        temp_trader = iris_native.classMethodValue("%PopulateUtils", "Name")
        temp_shares = randint(1, 10)
        print("New trade: {}, {}, {}, {}, {}"
              .format(temp_name, temp_date, temp_amount, temp_shares, temp_trader))


# Call routines directly
def call_routines(iris_native):
    print("on InterSystems IRIS version: " + iris_native.function("StocksUtil", "PrintVersion"))


# Execute task based on user input
def execute_selection(selection, iris_native):
    if selection == 1:
        set_test_global(iris_native)
    elif selection == 2:
        store_stock_data(iris_native)
    elif selection == 3:
        print_nodes(iris_native)
    elif selection == 4:
        generate_data(iris_native, 10)
    elif selection == 5:
        call_routines(iris_native)


# Get connection details from config file
def get_connection_info(file_name):
    # Initial empty dictionary to store connection details
    connections = {}

    # Open config file to get connection info
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            # remove all white space (space, tab, new line)
            line = ''.join(line.split())

            # get connection info
            connection_param, connection_value = line.split(":")
            connections[connection_param] = connection_value
    return connections


def run():
    # Retrieve connection information from configuration file
    connection_detail = get_connection_info("connection.config")

    ip = connection_detail["ip"]
    port = int(connection_detail["port"])
    namespace = connection_detail["namespace"]
    username = connection_detail["username"]
    password = connection_detail["password"]

    # Create connection to InterSystems IRIS
    connection = irisnative.createConnection(ip, port, namespace, username, password)

    print("Connected to InterSystems IRIS via the Native API")

    # Create an iris object
    iris_native = irisnative.createIris(connection)

    # Starting interactive prompt
    while True:
        print("1. Test")
        print("2. Store stock data")
        print("3. View stock data")
        print("4. Generate Trades")
        print("5. Call routine")
        print("6. Quit")
        selection = int(input("What would you like to do? "))
        if selection == 6:
            break
        elif selection not in range(1, 7):
            print("Invalid option. Try again!")
            continue
        execute_selection(selection, iris_native)


if __name__ == '__main__':
    run()



""" while 1:
    user_input = input(">> ")
    if input == 'exit':
        ser.close()
        exit()

    elif user_input == "on":
        ser.write("on".encode())
        print(ser.readline().decode())
        time.sleep(.1)

    elif user_input == "off":
        ser.write("off".encode())
        print(ser.readline().decode())
        time.sleep(.1)
    else:
        print("Invalid command")
        time.sleep(.1) """
def prime(num):
    re = True
    for i in range(2, num):
        if num % i == 0:
            re = False

    return re

def decom(num, type="str"):

    lst = []
    
    
    if type == "str":
        answer = ""
        while num != 1:
            for i in range(2, int(num + 1)):
                if num % i == 0 and prime(i):
                    if answer == "":
                        answer += str(i)

                    else:
                        answer += " x " + str(i)
                
                    num = num / i
                    break
        return answer

    else:
        while num != 1:
            for i in range(2, int(num + 1)):
                if num % i == 0 and prime(i):
                    lst.append(i)
                
                    num = num / i
                    break
        return lst

def factorial(number):
    num = 1
    for i in range(1, number + 1):
        num = num * i

    return num

def absolute(number):
    if number < 0:
        number = - number

    return number

def inverse(number):
    m = 0
    while number != 0:
        m = m * 10 + number % 10
        number = number // 10

def numt(number):
    num = 0
    while number != 0:
        num = num + 1
        number = number // 10

    return num

def ninnum(main_number, search_number):
    num = 0
    for i in str(main_number):
        if int(i) == search_number:
            num = num + 1

    return(num)

def sumnum(number):
    num = 0
    while number != 0:
        num = num + number % 10
        number = number // 10

    return num

def lcm(number1, number2):
    for i in range(1, number1 * number2 + 1):
        if i % number1 == 0 and i % number2 == 0:
            return i
            break

def bigger(number1, number2):
    num = number1
    if number2 > number1:
        num = number2

    return num

def smaller(number1, number2):
    num = number1
    if number2 < number1:
        num = number2

    return num

def gcd(number1, number2):
    num = 1
    for i in range(1, bigger(number1, number2)):
        if number1 % i == 0 and number2 % i == 0:
            num = i

    return num

def sqrt(num):
    return num ** 0.5

def pi_num():
    return 3.14159265359
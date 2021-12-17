import timeit
import random


def counting_sort_partial(array):
    '''
    This function is an adaptation of counting sort which instead of returning a sorted array
    it returns the position array.
    Complexity: O(n + m) where n is the length of the input array and m is the maximum element in the array
    :param array: The input array for which the position array is returned
    :return: The position array containing the position of each element
    '''
    maxElement = max(array)
    countElements = [0] * (maxElement+1)
    position = [0] * (maxElement+1)

    # a for loop using to count the number of elements that are the same
    for x in range(len(array)):
        countElements[array[x]] += 1

    # a for loop used for getting the position of each value
    for i in range(1, maxElement+1):
        position[i] = position[i-1] + countElements[i-1]

    return position


def digits_in_base(number, base):
    '''
    This function returns the number of digits in an integer represented in base
    :param number: The number to return the digits in base
    :param base: The base to represent the number in
    :return: The number of digits in number represented in base base
    '''
    remainder = number // base
    number_of_digits = 1
    while remainder != 0:
        number_of_digits += 1
        remainder = remainder // base
    return number_of_digits

def radix_sort(list, base):
    '''
    This is an implementation of radix sort which uses the counting_sort_partial adaptation to sort elements by the nth
    digit in the specified base.
    Complexity: O((n + b)M) where n is the total number of integers in the input, b is the base and M is the number of
    digits in the maximum number represented in base b
    :param list: A list of integers to be sorted
    :param base: A base to represent each number in to sort each digit by
    :return: a sorted list of integers
    '''

    # If the list is empty return the list
    if len(list) == 0:
        return list

    # setup the variables used in radix sort
    output = [0]*len(list)
    temp = [0]*len(list)
    max_number = max(list)
    max_number_length = digits_in_base(max_number, base)
    list_copy = []

    # create a copy of the input so it remains unaffected
    for item in list:
        list_copy.append(item)

    # for d between 0 and the number of digits in the max number represented in base
    for d in range(0, max_number_length):

        # create a temp array with the d-th digit of each element in it
        for x in range(len(list_copy)):
            temp[x] = list_copy[x] // base ** d % base

        # perform counting_sort_partial on the temp array
        position = counting_sort_partial(temp)

        # move each element depending on the position array
        for i in range(len(temp)):
            output[position[temp[i]]] = list_copy[i]
            position[temp[i]] += 1

        # copy the result of this iteration into the copy of the original list
        for i in range(len(output)):
            list_copy[i] = output[i]

    # return the output
    return output


def time_radix_sort():
    '''
    This function is used to time radix sort on a wide range of bases using random input data.
    :return results: a list of tuples representing the base used and the time recorded for that base.
    '''
    test_data = [random.randint(1, (2 ** 64) - 1) for _ in range(100000)]
    bases = [2, 7, 10, 21, 179, 256, 999, 100000, 171707, 10000019, 139589338]
    results = []
    for base in bases:
        print(base)
        start_has_time = timeit.default_timer()
        radix_sort(test_data, base)
        results.append((base, timeit.default_timer() - start_has_time))
    return results


def radix_sort_rotations(list):
    '''
    This is an adaptation of radix sort which uses the counting_sort_partial adaptation to sort elements by the nth
    character by its ascii value.
    Complexity: O(NM) where n is the total number of strings in the input and M is the number of
    characters in the longest string.
    :param list: A list of strings to be sorted
    :return: a sorted list of strings
    '''
    if len(list) == 0:
        return list

    output = [0]*len(list)
    temp = [0]*len(list)
    max_number_length = len(max(list))
    list_copy = []

    for item in list:
        list_copy.append(item)

    for d in range(0, max_number_length):

        # copying the dth character in the string to the temp array

        for x in range(len(list_copy)):
            # if d is less than the current string length
            if d < len(list_copy[x]):
                # add the character to the temp array
                temp[x] = list_copy[x][d]
            else:
                # add a character with an ascii value less than 'a'
                temp[x] = '.'

        # use list comprehension to convert all characters to the ascii value
        temp = [ord(i) for i in temp]

        # perform counting sort on the ascii values
        position = counting_sort_partial(temp)

        # move each element in the output array depending on the value in position
        for i in range(len(temp)):
            output[position[temp[i]]] = list_copy[i]
            position[temp[i]] += 1

        # copy the output array into the list_copy array to repeat the process for other characters
        for i in range(len(output)):
            list_copy[i] = output[i]

    return output


def find_rotations(list, p):
    '''
    This function takes a list of strings and a number p and returns all occurrences of the p rotation of each
    string in the original list and returns them
    Complexity: O(NM) Where N is the number of strings in the input list and M is the number of characters in the
    longest string
    :param list: A list of strings
    :param p: A number representing the number of rotations
    :return: The strings in the original list whose p rotations also exist
    '''
    # an array to hold the rotated strings
    rotated = []
    # for each string in the list
    for string in list:
        # if the rotation is positive
        if p > 0:
            # find the number of rotations for the current string
            num_rotations = p % len(string)
            # append the rotated string to rotated
            rotated.append(string[num_rotations:] + string[0:num_rotations])
        # if the rotation is negative
        elif p < 0:
            # find the number of rotations for the current string
            num_rotations = (p*-1) % len(string)
            # rotate the strings and append to rotated
            rotated.append(string[len(string) - num_rotations:] + string[0: len(string) - num_rotations])

    # use radix sort to sort a list containing the rotated and unrotated strings in O(MN)
    final = radix_sort_rotations(rotated + list)
    output = []

    # Strings that are the same will be positioned next to each other after sorting.
    # check if the i-1 string is the same as the ith string. if so append to output
    for i in range(1, len(final)):
        if final[i-1] == final[i]:
            output.append(final[i])

    # return the strings to the original form found in the input list
    if p > 0:
        output = [string[len(string) - num_rotations:] + string[0: len(string) - num_rotations] for string in output]
    elif p < 0:
        output = [string[num_rotations:] + string[0:num_rotations] for string in output]

    return output


time_radix_sort()
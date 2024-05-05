# kasiski_attack.py
#
# Author: Ralph Gootee <rgootee@gmail.com>
# Modified by:
# 	- David Fraga Rodríguez <david.fraga.rodriguez@udc.es>
# 	- María Rey Escobar <maria.rescobar@udc.es>

from sys import argv  # for command line arguments
from math import gcd  # euclidian algorithm
from functools import reduce
from collections import deque
from numpy import linalg, asarray


def calc_key_length(string, gram_length):
    """
    Calculates the suggested passkey length of the string using Kasiski
    """

    locations = []
    distances = []

    # locate all grams
    for i in range(len(string)):
        gram = string[i : i + gram_length]

        # make sure we don't get stuck with shorties
        if len(gram) < gram_length:
            break

        locations.append([])

        find = string.find(gram, 0)
        while find != -1:
            locations[i].append(find)
            find = string.find(gram, find + 1)

        # only calculate the distances if needed
        if len(locations[i]) > 1:
            for j in range(1, len(locations[i])):
                distances.append(locations[i][j] - locations[i][0])

    return reduce(gcd, distances)


def construct_y(string, key_length):
    """
    Constructs the Y_i vectors of string

    Input Arguments:
        string -- the ciphertext
        keyLength -- the passkey length

    """

    # figure this out
    y = [""] * key_length

    for i in range(len(string)):
        y[i % key_length] += string[i]

    return y


def calc_mg(y, alfab, prob):
    """
    Calculates the M_g value for a given string vector
    """

    fre = deque([0] * len(alfab))
    for i in range(len(alfab)):
        fre[i] = y.count(alfab[i])

    mg = [0] * len(alfab)
    for g in range(len(alfab)):
        suma = 0
        for i in range(len(alfab)):
            suma += prob[i] * fre[i]
        mg[g] = suma / len(y)
        fre.rotate(-1)

    return mg


def attack(string, key_length, prob, alfab):
    # construct y[i]
    y = construct_y(string, key_length)

    # calculate Mg
    mg = []
    for i in range(key_length):
        m = calc_mg(y[i], alfab, prob)
        mg.append(m)

    # suggest the key
    key = ""
    for i in range(key_length):
        key += alfab[mg[i].index(max(mg[i]))]

    return key


def detect_language(string):
    """
    Detects the language of the input string based on character frequency.
    """

    # Count the frequency of each character
    freq = {}
    for char in string:
        freq[char] = freq.get(char, 0) + 1

    # Sort frequencies in descending order
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    # Define language based on the most frequent characters
    if sorted_freq[0][0] in "ETAOINSHRD":
        return "English"
    elif sorted_freq[0][0] in "EASIONRT":
        return "Spanish"
    elif sorted_freq[0][0] in "ETAINOSRL":
        return "French"
    else:
        return "Unknown"


def main():
    """Probabilidades por cada idioma"""
    prob_ENG = [
        0.08167,
        0.01492,
        0.02782,
        0.04253,
        0.12702,
        0.02228,
        0.02015,
        0.06094,
        0.06966,
        0.00153,
        0.00772,
        0.04025,
        0.02406,
        0.06749,
        0.0,
        0.07507,
        0.01929,
        0.00095,
        0.05987,
        0.06327,
        0.09056,
        0.02758,
        0.00658,
        0.0236,
        0.0015,
        0.01654,
        0.00074,
    ]
    prob_SPN = [
        0.1216,
        0.0149,
        0.0387,
        0.0467,
        0.1408,
        0.0069,
        0.01,
        0.018,
        0.0598,
        0.0052,
        0.0011,
        0.0524,
        0.0308,
        0.07,
        0.0,
        0.092,
        0.0289,
        0.0111,
        0.0641,
        0.072,
        0.046,
        0.0469,
        0.0105,
        0.0004,
        0.0014,
        0.0109,
        0.0047,
    ]
    prob_FRN = [
        0.08173,
        0.00901,
        0.03345,
        0.03669,
        0.16716,
        0.01066,
        0.00866,
        0.00737,
        0.07579,
        0.00613,
        0.0074,
        0.05456,
        0.02968,
        0.07095,
        0.0,
        0.05837,
        0.02521,
        0.01362,
        0.0693,
        0.07948,
        0.07244,
        0.06429,
        0.01838,
        0.00049,
        0.00427,
        0.00128,
        0.00326,
    ]

    with open(argv[1], "r", encoding="utf8") as f:
        message = f.read()

    # Detect the language of the message
    detected_language = detect_language(message)

    # Choose the probabilities and alphabet based on the detected language
    if detected_language == "English":
        prob = prob_ENG
        alfab = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    elif detected_language == "Spanish":
        prob = prob_SPN
        alfab = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    elif detected_language == "French":
        prob = prob_FRN
        alfab = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Calculate the key length
    gram_length = 6
    key_length = calc_key_length(message, gram_length)

    # Perform the attack and get the key
    key = attack(message, key_length, prob, alfab)

    # Print the key
    print("Suggested Passkey:", key)


if __name__ == "__main__":
    main()

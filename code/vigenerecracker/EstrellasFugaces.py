# kasiski_attack.py
#
# Author: Ralph Gootee <rgootee@gmail.com>
# Modified by:
#	- David Fraga Rodríguez <david.fraga.rodriguez@udc.es>
#	- María Rey Escobar <maria.rescobar@udc.es>

#-------------------------------------------------------------------------------
from sys import argv
from math import gcd
from functools import reduce
from collections import deque
from numpy import linalg, asarray


# -------------------------------------------------------------------------------
def calc_key_length(string, gram_length):
    """Calculates the suggested passkey length of the string using Kasiski"""

    locations = []
    distances = []

    # locate all grams
    for i in range(len(string)):
        gram = string[i:i + gram_length]

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
    y = [''] * key_length

    # Mete cada letra del texto en la posicion de la letra de la clave que la cifro
    for i in range(len(string)):
        y[i % key_length] += string[i]

    return y

def calc_mg(y, alfab, prob):
    """calculates the M_g value for a given string vector"""

    # frequency & probability
    fre = deque([0] * len(alfab))
    for i in range(len(alfab)):
        fre[i] = y.count(alfab[i])

    mg = [0] * len(alfab)
    for g in range(len(alfab)):
        suma = 0
        for i in range(len(alfab)):
            suma += prob[i] * fre[i]  # Probabilidad de letra por numero de ocurrencias
        mg[g] = suma / len(y)  # Se divide el sumatorio entre la longitud de y
        fre.rotate(-1)  # Desplazamiento a la izquierda

    return mg

# Hackeo de clave
def attack(string, key_length, prob):
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

""" Probabilidades por cada idioma """
prob_ENG = [.08167, .01492, .02782, .04253, .12702, .02228, .02015, .06094, .06966, .00153, .00772, .04025, .02406,
            .06749, .0, .07507, .01929, .00095, .05987, .06327, .09056, .02758, .00658, .0236, .0015, .01654, .00074]
prob_SPN = [.1216, .0149, .0387, .0467, .1408, .0069, .01, 0.018, .0598, .0052, .0011, .0524, .0308, .07, .0, .092,
            .0289, .0111, .0641, .072, .046, .0469, .0105, .0004, .0014, .0109, .0047]
prob_FRN = [.08173, .00901, .03345, .03669, .16716, .01066, .00866, .00737, .07579, .00613, .0074, .05456, .02968,
            .07095, .0, .05837, .02521, .01362, .0693, .07948, .07244, .06429, .01838, .00049, .00427, .00128, .00326]

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
    
# Get the input message
message = input("Enter the encrypted message: ")

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
key = attack(message, key_length, prob)

# Print the key
print("Decrypted Key:", key)
import random
from math import gcd, ceil

n = None
phi = None
public_key = None
private_key = None

# A simple function to check if a number is prime
def is_prime(a):
    count = 0
    for i in range(2, ceil(a/2)+1):
        if a % i == 0:
            count += 1
            break
    if count == 0:
        return a

# Randomly choose two very large co-prime numbers (1024bits ~ 128 characters approx)
# Keep secret and delete after formation of the key pair
def generate_rand_nos(lower_lim, upper_lim):
    if lower_lim == 1: lower_lim += 1
    primes = [i for i in range(lower_lim, upper_lim) if is_prime(i)]
    p = random.choice(primes)
    q = random.choice(primes)
    if p == q:
        q = random.choice(primes)
    return p, q

def generate_pub_key(n, phi):
    # Generating a list of possible public keys.
    possible_pub_keys = [num for num in range(2, n) if gcd(num, phi) == 1]
    # Above list comprehension in expanded below just for explanation pusposes. 
    """
    possible_pub_keys = []
    for num in range(2,n):
        if gcd(num,phi) == 1:
            possible_pub_keys.append(num)
    """
    return random.choice(possible_pub_keys)

def generate_priv_key(public_key, phi):
    # Generating the list of all possible private keys using the "Extended euclidian algorithm"
    priv_keys = [i for i in range(1, phi*100) if (public_key * i) % phi == 1]
    # returning a private key randomly chosen from the above list
    return random.choice(priv_keys)

def encrypt(plaintext):
    global n
    global phi
    global public_key
    if public_key == None:
        # generating radom numbers by calling the generate_rand_nos function
        p, q = generate_rand_nos(1, 100)
        # used a modulus to keep the length of the key fixed
        n = p * q 
        # determining the value of phi 
        phi = ceil((p-1)*(q-1) / gcd(p-1, q-1))
        public_key = generate_pub_key(n, phi)
        print("Public key: ({}, {})".format(public_key, n))
    return (plaintext ** public_key) % n

def decrypt(ciphertext, priv_key = None, pq = None):
    global n
    global phi
    global public_key
    global private_key
    # The below if conditions just help if we are supplying random arguments to the encrypt function
    if pq:
        n = pq
    if priv_key:
        private_key = priv_key
        print("Private key: ({}, {})".format(private_key, n))
    elif private_key == None:
        private_key = generate_priv_key(public_key, phi)
        print("Private key: ({}, {})".format(private_key, n))
    return (ciphertext ** private_key) % n

# taking a message as input from the user
message = list((input("Enter the message: ")).encode())

# encrypting the message and appending each byte to the list "ciphertext"
ciphertext = [encrypt(num) for num in message]

# decrypting the message and appending each byte to the list "deciphered" 
deciphered = [chr(decrypt(cipher)) for cipher in ciphertext]

# Just the printing stuff
var = [chr(i) for i in ciphertext]
print("Ciphertext:", "".join(var))
print("Deciphered:", "".join(deciphered))

# comment out the above code and uncomment the below line if you just want to decrypt and possess a private key
# USAGE: decrypt(cipher_text, private_key, n)
#print(decrypt(44966, 598063, 81617))
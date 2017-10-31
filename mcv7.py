#!/usr/bin/python3.5
import os, shutil, sys, re, pyperclip, argparse
from time import sleep

#Master Crypt Version 7   #I know, the name sucks but I needed to name it something.
#By, codeDirtyToMe
#Started 26 Feb 2017
"""This program will attempt to encrypt and decrypt text via a Vigenere cipher with out having to code
an entire matrix of shift ciphers. It will have the ability to encrypt and decrypt interactively or by
file."""

"""As of 18 March 2017, the interactive encryption/decryption works fine.  As of 5 April 2017, 
transposition functionality was added."""

"""As of 15 April, the ability to input and output via files was added."""

"""As of 11 May 2017, the ability to add the enciphered or deciphered text to the clipboard was 
added. This is particularly useful testing the program as I don't have to manually copy the cipher/plain
text."""

"""As of 18 June 2017, I've started to add the ability to use REAL options and arguments. I've got it
working just well enough to use in my IPupdater.sh. I need to come back and tighten it up still."""

"""As of 14 July 2017, I've removed the ability to pass a message to it directly via the CLI.
Instead, a message must be passed via file. This was done in order to prevent issues arising from
argparse parsing illegal characters in my plain/cipher text alphabets. As on now, it is working
well with my IPupdater script. I'm sure there are still bugs in it though."""

"""As of 17 July 2017, I've increased the security of the cipher by making it a real Vigenere cipher."""

"""I would like to add the ability to add a salt to the encrypted data. With Python being a scripted 
language, it may be hard to keep it secure. A compiled language may be better for salts. I'll check it 
out either way."""

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filein", type=str, help="\"message to be enciphered or deciphered.\"")
parser.add_argument("-k", "--key", type=str, help="Encryption/Decryption key. Put in quotes if white space is included.")
parser.add_argument("-e", "--encrypt", help="encrypt the message", action="store_true")
parser.add_argument("-d", "--decrypt", help="decrypt the message", action="store_true")
parser.add_argument("-c", "--clip", help="output to clipboard", action="store_true")
parser.add_argument("-t", "--trans", help="apply transposition or de-transposition", action="store_true")
parser.add_argument("-n", "--nooutput", help="Do NOT output to file", action="store_true")
parser.add_argument("-z", "--noclip", help="Do NOT output to clipboard", action="store_true")
arguments = parser.parse_args()

argFileIn = arguments.filein
argEncrypt = arguments.encrypt
argDecrypt = arguments.decrypt
argClip = arguments.clip
argTrans = arguments.trans
argKey = arguments.key
argNoOutput = arguments.nooutput
argNoClip = arguments.noclip

#####################################################################################################################

def encrypt(workingEncryptText = []) :
    #Test for which input method was used and load the working variable equal to that parameter.
    if len(workingEncryptText) > 0 :
        plainTextMessage = workingEncryptText
    else :
        print('Error. No data passed.')
        main()

    encryptedMessage = list()
    encryptionKey = list()

    #Test for whether or not user input is needed.
    if argFileIn is not None :
        if arguments.key:
            encryptionKey = list(arguments.key)
        else :
            print("No argument given for -k option.")
            exit(1)
    else : #No arguments from the -m option were passed.
        encryptionKey = list(input('\nEnter the encryption key: '))

    #Create a second list of unused characters from the plainTextAlpha.
    extraKeyChars = list()
    for z in range(len(plainTextAlpha)):
        if plainTextAlpha[z] in encryptionKey :
            continue
        else :
            extraKeyChars.append(plainTextAlpha[z])

    #Now we concatenate the encryption key with the unused characters. Then we multiply itself by the quotient of
    #the length of the plain text message and encryption key. This ensures that the encryption key will never be
    #out of scope in the following for loop.
    encryptionKey = encryptionKey + extraKeyChars
    encryptionKey *= int(len(plainTextMessage) / len(encryptionKey) + 1)

    for i in range(len(plainTextMessage)):
        encryptedMessage = encryptedMessage + [cipherTextAlpha[plainTextAlpha.index(plainTextMessage[i]) + cipherTextAlpha.index(encryptionKey[i])]]

    encryptedMessage = transpositionEncryption(encryptedMessage)
    outputQuestion(encryptedMessage)
    clipBoard(encryptedMessage)
    os.system('clear')
    print("\nEncrypted message: " + str("".join(encryptedMessage)))

    if argFileIn is not None :
        exit(0)
    else :
        main()

#####################################################################################################################

def decrypt(workingDecryptText = []) :
    #Test for which input method was used and load the working variable equal to that parameter.
    if len(workingDecryptText) > 0 :
        cipherTextMessage = workingDecryptText
        regexUsage = 1
    else :
        print('Error. No data passed.')
        main()

    decryptedMessage = []

    #Check for whether user interation is required.
    if argFileIn is not None :
        if argTrans is not None :
            deTranspositionChoice = "y"
        else :
            deTranspositionChoice = "n"
    else :
        deTranspositionChoice = input('Would you like to de-transpose this message? (y | n): ')

    if deTranspositionChoice == 'y' or deTranspositionChoice == 'Y' :
        cipherTextMessage = transpositionDecryption(cipherTextMessage)
    elif deTranspositionChoice =='n' or deTranspositionChoice == 'N' :
        print()
    else :
        print('Error in choice. Please select y or n.\n')
        decrypt()

    #Figure out the decryption key.
    if argFileIn is not None :
        decryptionKey = argKey
    else :
        decryptionKey = list(input('Enter the decryption key: '))

        # Create a second list of unused characters from the plainTextAlpha.
        extraDecryptKeyChars = list()
        for z in range(len(plainTextAlpha)):
            if plainTextAlpha[z] in decryptionKey:
                continue
            else:
                extraDecryptKeyChars.append(plainTextAlpha[z])

        # Now we concatenate the decryption key with the unused characters. Then we multiply itself by the quotient of
        # the length of the plain text message and decryption key. This ensures that the decryption key will never be
        # out of scope in the following for loop.
        decryptionKey = decryptionKey + extraDecryptKeyChars
        decryptionKey *= int(len(cipherTextMessage) / len(decryptionKey) + 1)

    for j in range(len(cipherTextMessage)) :
        decryptedMessage = decryptedMessage + [plainTextAlpha[cipherTextAlpha.index(cipherTextMessage[j]) - cipherTextAlpha.index(decryptionKey[j])]]

    if regexUsage == 1 :
        newLineInsertRegex = re.compile(r'/')
        decryptedMessage = "".join(decryptedMessage)
        decryptedMessage = newLineInsertRegex.sub('\n', decryptedMessage)
        outputQuestion(decryptedMessage)
        clipBoard(decryptedMessage)
        print(decryptedMessage)
        if argFileIn is not None :
            exit(0)
        else :
            main()
    else :
        print('\n' + "".join(decryptedMessage) + '\n')
        outputQuestion(decryptedMessage)
        clipBoard(decryptedMessage)
        if len(argMessage) > 0 :
            exit(0)
        else :
            main()

#####################################################################################################################

def outputQuestion(workingOutput = []) :
    #This decision structure will pass the appropriate parameter to the output file.
    if len(workingOutput) > 0 :
        outputMessage = workingOutput
    else :
        print('fucking errors and shit.')
        exit(1)

    if argNoOutput is not False : #If output is desired in the -o option.
        outDecision = "n"
    else :
        outDecision = input('Would you like to output to a file? (y | n): ')

    if outDecision == 'y' or outDecision == 'Y':
        #List the directory and it's contents.
        print('\nHere are the current files in the working directory:\n--------------------------------')
        print(os.listdir('.'))
        print('\nEnter a name for the file : ')
        fileOutputName = input()
        writeableFile = open(fileOutputName, 'w')
        outputMessage = "".join(outputMessage)
        writeableFile.write(outputMessage)
        writeableFile.close()
        print('File written succesfully.')
        sleep(2)
        os.system('clear')
        main()
    elif outDecision == 'n' or outDecision == 'N':
        #os.system('clear')
        return
    else :
        print('Sorry. Invalid input.')
        outputQuestion()

#####################################################################################################################

def transpositionEncryption(encryptedMessage) :
    if arguments.trans:
        transDecision = 'y'
    else :
        transDecision = input('Would you like to apply transposition? (y | n): ')

    if transDecision == 'n' or transDecision == 'N':
        return encryptedMessage
    elif transDecision == 'y' or transDecision == 'Y':
        trans1 = [] #First half of transposition
        trans2 = [] #Second half of transposition
        for t in range(len(encryptedMessage)) :
            if int(len(encryptedMessage) - (len(encryptedMessage) - int(t))) % 2 == 0 :
                trans1.append(encryptedMessage[t])
            else :
                trans2.append(encryptedMessage[t])
        encryptedMessage = "".join(trans2) + "".join(trans1)
        return encryptedMessage

#####################################################################################################################

def transpositionDecryption(substitutionDMsg) :
    deTransposedMessage = [] #Final de-transposed message.
    deTrans1 = [] #First half of de-transposition
    deTrans2 = [] #Second half of de-transposition

    if len(substitutionDMsg) % 2 == 0 :
        counter = int(len(substitutionDMsg) / 2)
        for g in range(int(len(substitutionDMsg) / 2)) :
            deTrans1.append(substitutionDMsg[g])

        while counter < int(len(substitutionDMsg)) :
            deTrans2.append(substitutionDMsg[counter])
            counter += 1

        for h in range(int(len(substitutionDMsg) / 2)) :
            if h % 2 == 0 :
                deTransposedMessage.append(deTrans2[h])
                deTransposedMessage.append(deTrans1[h])
            elif h % 2 != 0 :
                deTransposedMessage.append(deTrans2[h])
                deTransposedMessage.append(deTrans1[h])
        print('\n' + "".join(deTransposedMessage))
        return  deTransposedMessage
    elif len(substitutionDMsg) % 2 != 0 :
        counter = int(len(substitutionDMsg) / 2)
        for j in range(int(len(substitutionDMsg) / 2 + 1)) :
            deTrans1.append(substitutionDMsg[counter])
            counter += 1

        counter = 0 #Reset counter to 0 for the next loop.
        while counter < int(len(substitutionDMsg) / 2) : #This will run to the middle of the list.
            deTrans2.append(substitutionDMsg[counter])
            counter += 1

        for k in range(int(len(substitutionDMsg) / 2 + 1)) :
            if k % 2 == 0 :
                if k + 1 > len(deTrans2) :
                    deTransposedMessage.append(deTrans1[k])
                    break
                else :
                    deTransposedMessage.append(deTrans1[k])
                    deTransposedMessage.append(deTrans2[k])
            elif k % 2 != 0 :
                if k + 1 > len(deTrans2) :
                    deTransposedMessage.append(deTrans1[k])
                    break
                else :
                    deTransposedMessage.append(deTrans1[k])
                    deTransposedMessage.append(deTrans2[k])

        return deTransposedMessage
    else :
        exit(1)

#####################################################################################################################

def encipherORdecipher(workingEORD = []) : #Pass the text received from main() to the correct cryptography function.
    eORdDecision = input('Would you like to encipher or decipher the text? (e | d | exit): ')

    if eORdDecision == 'e' or eORdDecision == 'E':
        encrypt(workingEORD)
    elif eORdDecision == 'd' or eORdDecision == 'D':
        decrypt(workingEORD)
    elif eORdDecision == 'exit' or eORdDecision == 'EXIT':
        exit(0)
    else :
        os.system('clear')
        print('Sorry, invalid input. Try again.\n')
        encipherORdecipher(interactiveText, argumentText, listFileText)

#####################################################################################################################

def clipBoard(workingClip = []) :
    if len(workingClip) > 0 :
        clipBoardMessage = "".join(workingClip)
    else :
        print('Error.')
        exit(1)

    if argClip is not False :
        clipBoardDecision = "y"
    elif argNoClip is not False :
        clipBoardDecision = "n"
    else :
        clipBoardDecision = input('\nWould you like to send the text to the clipboard? (y | n) : ')

    if clipBoardDecision == 'y' or clipBoardDecision == 'Y':
        pyperclip.copy(clipBoardMessage)
        print('Text has been saved to the clipboard.')
        sleep(1)
        return
    elif clipBoardDecision == 'n' or clipBoardDecision == 'N':
        return
    else :
        print('Sorry, invalid input. Try again.\n')
        clipBoard(clipBoardMessage)

#####################################################################################################################

def fileWorks(fileText) :
    # Test document for existence
    if os.path.exists(fileText) == True:
        newLineRegex = re.compile(r'\n')  # Regex for removing newline feeds from string.
        # Open file and convet to list.
        openFileText = open(fileText)
        listFileText = openFileText.read()  # Convert to string.
        listFileText = newLineRegex.sub('/', listFileText)  # Replace newline feeds with a space.
        listFileText = list(listFileText)  # Convert to individual character list.
        openFileText.close()  # Close the file.
        return listFileText
    else:
        print('Sorry, the file does not exist. Either put the script in the same \n',
              'working directory or use the absolute path.\n')
        main()

#####################################################################################################################
def main() :
    #Check for arguments
    if len(sys.argv) > int(1) :
        if arguments.filein is not None :
            argumentText = fileWorks(arguments.filein)

            #Check for -e or -d options in order to bypass encipherORdecipher()
            if arguments.encrypt:
                encrypt(argumentText)
            elif arguments.decrypt:
                decrypt(argumentText)
            else :
                print("You must supply a -e or -d option.")
                exit(1)

        else :
            print("fucking errors and shit...")
            exit(1)
    else :
        print('\nmcv7: By, codeDirtyToMe\nThis script will encrypt text with a polyalphabetic',
              'Vigenere cipher. If a single shift \ncipher of 1 is desired, use a single character',
              'encryption key.\nTranspositon can also be applied.')
        print('Files can be supplied via arguments if desired.\n')
        decision = input('Would you like to use interactive or file mode? (i | f | exit): ')
        os.system('clear') #Clear screen
        if decision == 'i' or decision == 'I':
            print('\nEnter the plaintext that needs encryption.\nAcceptable characters include all lower and upper case letters\n'
                'as well as all numbers and normal punctuation marks:')
            interactiveText = input()
            interactiveText = list(interactiveText) #Convert to list.

            #Ask for encipherment or decipherment.
            encipherORdecipher(interactiveText)
        elif decision == 'f' or decision == 'F':
            #List the contents of the current working directory and ask for input.
            print('The files available in your directory are :\n' + str(os.listdir('.')))
            print('-------------------------------------------------------------------------')
            print('Which file would you like to work with? :')
            workingFileText = input()
            workingFileText = fileWorks(workingFileText)
            encipherORdecipher(workingFileText)
        elif decision == 'exit' or decision == 'EXIT':
            exit(0)
        else :
            print('Sorry, invalid input.')
            main()

################################################
#"""This is the actual start of the program."""#
################################################

#This will be the plaintext and cipher text alphabets used for encryption and decryption.
#The idea is to only use one of each. The shift will be based off a key word which is normal.
#The shift will be based of the index value of each individual char in the key.
#I should be able to use only one alphabet, but I'll stick to two seperate ones for now. I
#really just don't feel like figuring out how to loop back over to the beginning of the list...


plainTextAlpha = ['a','b','c','d','e','f','g','h','i','j',
                  'k','l','m','n','o','p','q','r','s','t',
                  'u','v','w','x','y','z',' ','.',',','?',
                  ';','"','!','-','_','/',':','@','#','$',
                  '%','&','*','=','\'','>','<','0','1','2',
                  '3','4','5','6','7','8','9','A','B','C',
                  'D','E','F','G','H','I','J','K','L','M',
                  'N','O','P','Q','R','S','T','U','V','W',
                  'X','Y','Z']

cipherTextAlpha = list()
cipherTextAlpha = plainTextAlpha + plainTextAlpha

main()
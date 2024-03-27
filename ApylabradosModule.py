import numpy as np
import pandas as pd
import csv


class Pawns():
    def __init__(self):
        self.letters = []

    def addPawn(self, c):
        """
        Añade una ficha c a la lista de caracteres letters

        Inputs
            c (str): Caracter a añadir
        """
        self.letters.append(c)


    def addPawns(self, c, n):
        """
        Añade n veces una ficha c a la lista de caracteres letters

        Inputs
            c (str): Caracter a añadir
            n (int): Numero de veces a añadir
        """
        for _ in range(n):
            self.addPawn(c)


    def createBag(self):
        """
        Crea una bolsa con todas las fichas iniciales
        """
        with open("/content/drive/MyDrive/Python - Udemy/Proyecto Final Apylabrados/bag_of_pawns.csv", "r") as f:
            reader = csv.reader(f)
            f.readline()
            for row in reader:
                self.addPawns(row[0], int(row[1]))


    def showPawns(self):
        """
        Muestra las fichas y su cantidad
        """
        # letras = list(set(self.letters))
        # letras = sorted(letras)
        # for c in letras:
        #     print("{}: {}".format(c, self.letters.count(c)))

        ft_pawns = self.getFrequency()
        ft_pawns.showFrequency()

    def takeRandomPawn(self):
        """
        Saca una ficha de la bolsa y se la coloca al jugador

        Outs:
            letter (str): Letra que se sacó
        """
        i = np.random.randint(0, self.getTotalPawns() - 1)
        letter = self.letters[i]
        self.letters.pop(i)
        return letter

    def getFrequency(self):
        """
        Muestra las frecuencias de las letras del objeto Pawns

        Outs:
            (FrecuencyTable object):

        """

        ft = FrequencyTable()
        for c in self.letters:
            ft.update(c)
        return ft

    def takePawn(self, c):
        self.letters.remove(c)

    def getTotalPawns(self):
        return len(self.letters)


class Word():
    def __init__(self):
        self.word = []

    def __str__(self):
        word_str = ""
        for c in self.word:
            word_str += c
        return(word_str)

    def areEqual(self, w):
        """
        Checa si dos palabras son iguales

        Ins:
            w (Word object): Palabra a comparar

        Outs:
            bool: Si son (T) o no son (F) iguales
        """
        return self.word == w.word

    def isEmpty(self):
        """
        Nos dice si una palabra está vacía

        Outs:
            bool: Si está (T) o no está (F) vacía
        """
        if self.word:
            return False
        return True

    @classmethod
    def readWord(cls):
        """
        Añade una palabra

        Outs:
            w (Word object): Palabra leída pasada a objeto
        """
        s = input("Introduce una palabra: ")
        w = Word()
        for c in s.upper():
            w.word.append(c)
        return w

    @staticmethod
    def readWordFromFile(f):
        """
        Lee una palabra de un fichero f

        Ins:
            f: Fichero del cual se debe leer

        Outs:
            converted_word: Palabra leída convertida a objeto Word
        """
        converted_word = Word()
        file_word = f.readline()
        for c in file_word[:-1]:
            converted_word.word.append(c)
        return converted_word

    def getFrequency(self):
        """
        Muestra las frecuencias de las letras del objeto Word

        Outs:
            (FrecuencyTable object):

        """
        ft = FrequencyTable()
        for c in self.word:
            ft.update(c)

        return ft

    def getLengthWord(self):
        """
        Devuelve la longitud de la palabra
        """
        return len(self.word)   

class Dictionary():
    filepath = "/content/drive/MyDrive/Python - Udemy/Proyecto Final Apylabrados/dictionary.txt"

    @staticmethod
    def validateWord(given_word):
        """
        Valida si la palabra se encuentra en el diccionario

        Ins:
            given_word (Word obj): Palabra a checar

        Outs:
            bool: Si está (T) o no (F) en el diccionario
        """
        with open(Dictionary.filepath, "r") as f:
            dictionary_word = Word.readWordFromFile(f)
            while not dictionary_word.isEmpty() and not given_word.areEqual(dictionary_word):
                dictionary_word = Word.readWordFromFile(f)

        if dictionary_word.isEmpty() and not dictionary_word.areEqual(given_word):
            print("Esa palabra no esta en el diccionario.")
            return False
        else:
            return True
        

class FrequencyTable():
    def __init__(self):
        self.letters = np.array(["A","B","C","D","E","F","G","H","I","J","K","L","M","N",
                        "O","P","Q","R","S","T","U","V","W","X","Y","Z"])
        self.frequencies = np.zeros(len(self.letters), dtype=int)

    def showFrequency(self):
        """
        Muestra la frecuencia de aparición de cada letra por palabra
        """
        print("Frequencies:\n")
        for i in range(len(self.frequencies)):
            if self.frequencies[i] != 0:
                print("{}: {}".format(self.letters[i], self.frequencies[i]))

    @staticmethod
    def isSubset(ftable1, ftable2):
        """
        Comprueba si una palabra es subconjunto de otra

        Ins:
            ftable1: Tabla de Frecuencias de la primer palabra
            ftable2: Tabla de Frecuencias de la segunda palabra

        Outs:
            bool: Dice si la primer palabra es (T) o no es (F) subconjunto de la segunda
        """
        for i in range(len(ftable1.letters)):
            if ftable1.frequencies[i] <= ftable2.frequencies[i]:
                continue;
            else:
                return False
        return True


    def update(self, c):
        """
        Añade 1 a la frecuencia del caracter indicado
        """
        self.frequencies[np.where(self.letters == c)[0]] += 1


class Board():
    def __init__ (self):
        self.board = [[" " for j in range(15)] for i in range(15)]
        self.total_words = 0
        self.total_pawns = 0

    def showBoard(self):
        """
        Muestra el tablero
        """
        print("\n", end = " ")

        for i in range(len(self.board)):
            print(" {}{} ".format(0 if i <=9 else "", i), end = "")
        print("\n")

        for i in range(len(self.board)):
            print("+---"*len(self.board) + "+")
            for j in range(len(self.board)):
                print("| " + self.board[i][j], end =" ")
            print("| {}{}".format(0 if i <=9 else "", i))
        print("+---"*len(self.board)+ "+")

    def placeWord(self, player_pawns, word, x, y, direction):
        """
        Coloca la palabra en el tablero, elimina las fichas del jugador
        """
        for c in word.word:
            if self.board[x][y] != c: 
                self.board[x][y] =  c
                player_pawns.takePawn(c)
                self.total_pawns += 1

            if direction == "V":
                x += 1
            elif direction == "H":
                y += 1
            
        self.total_words += 1

    def isPossible(self, word, x, y, direction):
        """
        Comprueba si es posible colocar la palabra en la posición y coordenadas
        """
        message = ""
        size = word.getLengthWord()

        # Casilla Central
        if self.total_words == 0:
            message = "Ninguna ficha pasa por la casilla central"
            
            if direction == "H":
                if x != 7:
                    return (False, message)
                elif 7 not in range(y,y+size):
                    return (False, message)
            
            elif direction == "V":
                if y != 7:
                    return (False, message)
                elif 7 not in range(x,x+size):
                    return (False, message)

        else:

        # Límites del tablero
            message = "La palabra se sale de los límites del tablero"
            if x<0 or x>14 or y<0 or y>14:
                return(False, message)
            if direction == "V" and  x+size -1 > 14:
                return(False, message)
            if direction == "H" and  y+size-1 > 14:
                return(False, message)

        # Ficha existente
            message = "Debes usar una ficha existente"
            if direction == "V":
                for i in range(x, x+size):
                    if self.board[i][y] != " ":
                        break
                else:
                    return(False, message)
            if direction == "H":
                for i in range(y, y+size):
                    if self.board[x][i] != " ":
                        break
                else:
                    return(False, message)

            # Casilla ocupada
            x_copy = x
            y_copy = y
            for c in word.word:
                if self.board[x_copy][y_copy] != " " and self.board[x_copy][y_copy] != c:
                    message = "¡Ya hay una ficha distinta en una posicion que intentaste!"
                    return(False,message)
                if direction == "V":
                    x_copy += 1
                elif direction == "H":
                    y_copy += 1

            # Nueva ficha
            x_copy = x
            y_copy = y
            for c in word.word:
                if self.board[x_copy][y_copy] == " ":
                    break;
                if direction == "V":
                    x_copy += 1
                elif direction == "H":
                    y_copy += 1
            else: 
                message = "No has usado una nueva casilla"
                return(False,message)
            
            # No arruinar otra palabra
            message = "Hay fichas adicionales a principio o a final de palabra"
            size_fixed = size-1
            
            if direction == "V" and ((x != 0 and self.board[x-1][y] != " ") or (x + size != 14 and self.board[x + size][y] != " ")):
                return(False,message)
            
            if direction == "H" and ((y != 0 and self.board[x][y-1] != " ") or (y + size != 14 and self.board[x][y+size] != " ")):
                return(False,message)
        message = "Valido"
        return (True, message)

    def getPawns(self, word, x, y, direction):
        """
        Dice que fichas se necesitan para insertar una palabra en cierta posición y dirección
        """

        possible, message = self.isPossible(word,x,y,direction)
        if not possible:
            print(message)

        else:
            needed_letters = Word()
            for c in word.word:
                if self.board[x][y] != c:
                    needed_letters.word.append(c)
                if direction == "V":
                    x += 1
                elif direction == "H":
                    y += 1
            
        return needed_letters
        

import tensorflow as tf
import numpy as np
import abc


# Klasy funkcji aktywacji
class InterfaceFunkcjiAktywacji(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def funkcja_aktywacji( self, dane_wejsciowe ):
        """ metoda musi być nadpisana i ma zwracać funkcję aktywacji dla sieci """
    
class KlasaFunkcjiAktywacjiTan(InterfaceFunkcjiAktywacji):
    def funkcja_aktywacji( self, dane_wejsciowe ):
        L1 = tf.tanh(tf.matmul( dane_wejsciowe, layer1_attribs['wagi']) + layer1_attribs['biasy'])
        L2 = tf.tanh(tf.matmul(L1, layer2_attribs['wagi']) + layer2_attribs['biasy'])
        return tf.multiply(tf.add(L2, 1), 0.5)

class KlasaFunkcjiAktywacjiSigmoid(InterfaceFunkcjiAktywacji):
    def funkcja_aktywacji( self, dane_wejsciowe ):
        L1 = tf.sigmoid(tf.matmul(dane_wejsciowe, layer1_attribs['wagi']) + layer1_attribs['biasy'])
        return tf.sigmoid(tf.matmul(L1, layer2_attribs['wagi']) + layer2_attribs['biasy'])

class KlasaFunkcjiAktywacjiSLiniowa(InterfaceFunkcjiAktywacji):
    def funkcja_aktywacji( self, dane_wejsciowe ):
        L1 = tf.add( tf.matmul(dane_wejsciowe, layer1_attribs['wagi']), layer1_attribs['biasy'])
        L2 = tf.add( tf.matmul(tf.nn.relu(L1), layer2_attribs['wagi']),  layer2_attribs['biasy'])
        return tf.nn.relu(L2)

# dane treningowe
train_data = [[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]]

# spodziewane wyniki dla danych treningowych
label_data = [[0],
              [1],
              [1],
              [0]]

#if __name__ == '__main__':

# konfiguracja stałych
ILOSC_KROKOW_UCZENIA = 5000
SKOK_NAUKI = 0.1
JAK_CZESTO_POKAZAC_BLAD = 200
WYZEROWANY_BIAS = False

# konfiguracja warstw i ilosci neuronów
inputs_count = 2
nodes = {'L1': 50,
         'L2': 1}

# bufory na dane wejsciowe i wyjsciowe
X = tf.placeholder(tf.float32, shape=[len(train_data), inputs_count])
Y = tf.placeholder(tf.float32, shape=[len(label_data), nodes['L2']])

# atrybuty warstw i neuronów sieci 
layer1_attribs = { }
layer1_attribs['wagi'] = tf.Variable(tf.random_normal( [inputs_count, nodes['L1']] ))
layer1_attribs['biasy'] = tf.Variable(tf.zeros( [nodes['L1']] )) if WYZEROWANY_BIAS else tf.Variable(tf.random_normal( [nodes['L1']] ))

layer2_attribs = { }
layer2_attribs['wagi'] = tf.Variable(tf.random_normal( [nodes['L1'], nodes['L2']] ))
layer2_attribs['biasy'] = tf.Variable(tf.zeros( [nodes['L2']] )) if WYZEROWANY_BIAS else tf.Variable(tf.random_normal( [nodes['L2']] ))

# switcher funkcji aktywacji
def funkcja_aktywacji( dane_wejsciowe ):
    return (KlasaFunkcjiAktywacjiSLiniowa()).funkcja_aktywacji( tf.cast( dane_wejsciowe, tf.float32 ) )

# funkcja zwracająca wynik sieci dla danych
def mysl(dane_wejsciowe):
    return funkcja_aktywacji( dane_wejsciowe )
    
# funkcja liczaca blad sieci
def funkcja_delty( funkcja_myslenia, outputLabels ):
    return tf.nn.sigmoid_cross_entropy_with_logits( logits=funkcja_myslenia, labels=outputLabels )

# funkcja zmieniająca atrybuty sieci
def funkcja_propagacji( srednia_odleglosc_do_poprawnej_odpowiedzi ):
    return tf.train.AdamOptimizer(SKOK_NAUKI).minimize( srednia_odleglosc_do_poprawnej_odpowiedzi )
##    return tf.train.GradientDescentOptimizer(SKOK_NAUKI).minimize( srednia_odleglosc_do_poprawnej_odpowiedzi )

def ucz(X):
    # funkcja zwracająca wynik sieci dla danych
    wynik_myslenia = mysl(X) 

    # funkcja liczaca blad sieci
    funkcja_sigma = funkcja_delty( wynik_myslenia, Y )  

    # funkcja zwraca srednią arytmetyczną błędu sieci
    srednia_odleglosc_do_poprawnej_odpowiedzi = tf.reduce_mean( funkcja_sigma ) 

    # funkcja zmieniająca atrybuty sieci
    nauczyciel = funkcja_propagacji( srednia_odleglosc_do_poprawnej_odpowiedzi )
    
    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())

    # proces uczenia sieci
    for example_index in range(ILOSC_KROKOW_UCZENIA):
        # funkcja propagacji zmienia atrybuty sieci i zwraca aktualny błąd
        _, blad = sess.run( [ nauczyciel, srednia_odleglosc_do_poprawnej_odpowiedzi ]
                            , feed_dict = {X: train_data, Y: label_data})
        # wyswietlenie arytmetycznego bledu co N kroków
        if example_index % JAK_CZESTO_POKAZAC_BLAD == 0: print ("Sredni arytmetyczny blad sieci to ", blad)

# funkcja wyswietla dane treningowe i wyniki obliczen dla nich
def pokaz_obliczenia():
    print ("Dane treningowe: ", train_data)
    print ("Wyniki treningowe: \n", mysl(train_data).eval())

# funkcja wyswietla stan atrybutów sieci
def pokaz_atrybuty_warstw():
    print ("Atrybuty warstwy 1")
    print (layer1_attribs['wagi'].eval(), "\n", layer1_attribs['biasy'].eval())
    print ("Atrybuty warstwy 2")
    print (layer2_attribs['wagi'].eval(), "\n", layer1_attribs['biasy'].eval())
    
ucz(X)
pokaz_obliczenia()

#sess = tf.InteractiveSession()
#sess.run(tf.global_variables_initializer())

#print(mysl([[0, 1]]).eval())
    

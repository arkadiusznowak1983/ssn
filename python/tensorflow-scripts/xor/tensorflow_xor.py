import tensorflow as tf
import numpy as np
import abc


# Klasy warstw sieci AI
class TensorLayer(object):
    # stałe
    def ustawienia ( self, ustawienie = None ):
        def _ustawienia( ):
            return { 'WYZEROWANY_BIAS': False }
        
        if ustawienie == None:
            return None
        else:
            return _ustawienia()[ustawienie]

    # konstruktor warstwy
    def __init__( self, inputs_count, nodes ):
        self.layer = { }
        self.layer['wagi'] = tf.Variable(tf.random_normal( [inputs_count, nodes] ))
        self.layer['biasy'] = tf.Variable(tf.zeros([ nodes ])) if self.ustawienia( 'WYZEROWANY_BIAS' ) else tf.Variable(tf.random_normal([ nodes ]))
        self.layer['wyjscia'] = tf.Variable(tf.zeros([ nodes ]))

# Klasy funkcji aktywacji
class InterfaceFunkcjiAktywacji(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def funkcja_aktywacji( self, dane_wejsciowe, layers ):
        """ metoda musi być nadpisana i ma zwracać funkcję aktywacji dla sieci """

class KlasaFunkcjiAktywacjiTan(InterfaceFunkcjiAktywacji):
    def funkcja_aktywacji( self, dane_wejsciowe, layers ):
        L1 = tf.tanh(tf.matmul( dane_wejsciowe, layers[0].layer['wagi']) + layers[0].layer['biasy'])
        L2 = tf.tanh(tf.matmul(L1, layers[1].layer['wagi']) + layers[1].layer['biasy'])
        return tf.multiply(tf.add(L2, 1), 0.5)

class KlasaFunkcjiAktywacjiSigmoid(InterfaceFunkcjiAktywacji):
    def funkcja_aktywacji( self, dane_wejsciowe, layers ):
        L1 = tf.sigmoid(tf.matmul(dane_wejsciowe, layers[0].layer['wagi']) + layers[0].layer['biasy'])
        return tf.sigmoid(tf.matmul(L1, layers[1].layer['wagi']) + layers[1].layer['biasy'])

class KlasaFunkcjiAktywacjiSLiniowa(InterfaceFunkcjiAktywacji):
    def funkcja_aktywacji( self, dane_wejsciowe, layers ):
        L1 = tf.add( tf.matmul(dane_wejsciowe, layers[0].layer['wagi']), layers[0].layer['biasy'])
        L2 = tf.add( tf.matmul(tf.nn.relu(L1), layers[1].layer['wagi']), layers[1].layer['biasy'])
        return tf.nn.relu(L2)


class TensorNetwork(object):
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
    # bufory
    X = None
    Y = None
    
    def __init__(self):
        # konfiguracja warstw i ilosci neuronów
        self._layers = []
        self.inputs_count = 2
        self.nodes = {'L1': 50
                      ,'L2': 1}
        # konfiguracja stałych
        self.ILOSC_KROKOW_UCZENIA = 5000
        self.SKOK_NAUKI = 0.1
        self._JAK_CZESTO_POKAZAC_BLAD = 200

        # bufory na dane wejsciowe i wyjsciowe
        self.X = tf.placeholder(tf.float32, shape=[len(self.train_data), self.inputs_count])
        self.Y = tf.placeholder(tf.float32, shape=[len(self.label_data), self.nodes['L2']])

        # wygenerowanie warstw
        self._layers.append(TensorLayer( self.inputs_count, self.nodes['L1'] ))
        self._layers.append(TensorLayer( self.nodes['L1'], self.nodes['L2'] ))

    @property
    def layers(self): return self._layers

    @property
    def jakCzestoBlad(self): return self._JAK_CZESTO_POKAZAC_BLAD

    @jakCzestoBlad.setter
    def jakCzestoBlad(self, value): self._JAK_CZESTO_POKAZAC_BLAD = value

    @layers.setter
    def layers(self, value): return self._layers.append(value)
    
    # switcher funkcji aktywacji
    def funkcja_aktywacji( self, dane_wejsciowe ):
        return (KlasaFunkcjiAktywacjiSLiniowa()).funkcja_aktywacji( tf.cast( dane_wejsciowe, tf.float32 ), self._layers )

    # funkcja zwracająca wynik sieci dla danych
    def mysl( self, dane_wejsciowe ):
        return self.funkcja_aktywacji( dane_wejsciowe )
        
    # funkcja liczaca blad sieci
    def funkcja_delty( self, funkcja_myslenia, outputLabels ):
        return tf.nn.sigmoid_cross_entropy_with_logits( logits=funkcja_myslenia, labels=outputLabels )

    # funkcja zmieniająca atrybuty sieci
    def funkcja_propagacji( self, srednia_odleglosc_do_poprawnej_odpowiedzi ):
        return tf.train.AdamOptimizer(self.SKOK_NAUKI).minimize( srednia_odleglosc_do_poprawnej_odpowiedzi )
    ##    return tf.train.GradientDescentOptimizer(SKOK_NAUKI).minimize( srednia_odleglosc_do_poprawnej_odpowiedzi )

    def ucz( self, X ):
        Y = self.Y
        
        # funkcja zwracająca wynik sieci dla danych
        wynik_myslenia = self.mysl(X) 

        # funkcja liczaca blad sieci
        funkcja_sigma = self.funkcja_delty( wynik_myslenia, Y )  

        # funkcja zwraca srednią arytmetyczną błędu sieci
        srednia_odleglosc_do_poprawnej_odpowiedzi = tf.reduce_mean( funkcja_sigma ) 

        # funkcja zmieniająca atrybuty sieci
        nauczyciel = self.funkcja_propagacji( srednia_odleglosc_do_poprawnej_odpowiedzi )
        
        sess = tf.InteractiveSession()
        sess.run(tf.global_variables_initializer())

        # proces uczenia sieci
        for example_index in range(self.ILOSC_KROKOW_UCZENIA):
            # funkcja propagacji zmienia atrybuty sieci i zwraca aktualny błąd
            _, blad = sess.run( [ nauczyciel, srednia_odleglosc_do_poprawnej_odpowiedzi ]
                                , feed_dict = {X: self.train_data, Y: self.label_data})
            # wyswietlenie arytmetycznego bledu co N kroków
            if example_index % self.jakCzestoBlad == 0: print ("Sredni arytmetyczny blad sieci to ", blad)

    # funkcja wyswietla dane treningowe i wyniki obliczen dla nich
    def pokaz_obliczenia():
        print ("Dane treningowe: ", self.train_data)
        print ("Wyniki treningowe: \n", self.mysl(self.train_data).eval())

    # funkcja wyswietla stan atrybutów sieci
    def pokaz_atrybuty_warstw():
        print ("Atrybuty warstwy 1")
        print (self._layers[0].layer['wagi'].eval(), "\n", self._layers[0].layer['biasy'].eval())
        print ("Atrybuty warstwy 2")
        print (self._layers[1].layer['wagi'].eval(), "\n", self._layers[1].layer['biasy'].eval())


ssnObj = TensorNetwork()
ssnObj.ucz(ssnObj.X)
#ssnObj.pokaz_obliczenia()

#if __name__ == '__main__':
    #ssnObj = TensorNetwork()
        
#    ssnObj.ucz(ssnObj.X)
#    ssnObj.pokaz_obliczenia()

    #sess = tf.InteractiveSession()
    #sess.run(tf.global_variables_initializer())

    #print(mysl([[0, 1]]).eval())
        

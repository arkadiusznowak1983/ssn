import tensorflow as tf
from tensorflow.examples. tutorials.mnist import input_data

mnist = input_data.read_data_sets('t:\\', one_hot=True)

n_nods_hl1 = 500
n_nods_hl2 = 500
n_nods_hl3 = 500

n_class = 10
batch_size = 10

x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

def ssn_model(data):
    hidd_1_layer = {'wagi': tf.Variable(tf.random_normal([784, n_nods_hl1])),
                    'biasy': tf.Variable(tf.random_normal( [n_nods_hl1] ))}

    hidd_2_layer = {'wagi': tf.Variable(tf.random_normal([n_nods_hl1, n_nods_hl2])),
                    'biasy': tf.Variable(tf.random_normal( [n_nods_hl2] ))}

    hidd_3_layer = {'wagi': tf.Variable(tf.random_normal([n_nods_hl2, n_nods_hl3])),
                    'biasy': tf.Variable(tf.random_normal( [n_nods_hl3] ))}

    output_layer = {'wagi': tf.Variable(tf.random_normal([n_nods_hl3, n_class])),
                    'biasy': tf.Variable(tf.random_normal( [n_class] ))}    

    l1 = tf.add(tf.matmul(data, hidd_1_layer['wagi']), hidd_1_layer['biasy'])
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1, hidd_2_layer['wagi']), hidd_2_layer['biasy'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidd_3_layer['wagi']), hidd_3_layer['biasy'])
    l3 = tf.nn.relu(l3)

    return tf.matmul(l3, output_layer['wagi']) + output_layer['biasy']

    
def trenuj(x):
    wynik = ssn_model(x)
    blad_delta = tf.reduce_mean( tf.nn.sigmoid_cross_entropy_with_logits(logits=wynik, labels=y) )
    
    trener = tf.train.AdamOptimizer().minimize( blad_delta )

    ilosc_cykli = 10

    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())

    for cykl in range(ilosc_cykli):
        blad_suma = 0
        for _ in range(int(mnist.train.num_examples/batch_size)):
            ex, ey = mnist.train.next_batch( batch_size )
            _, blad = sess.run( [trener, blad_delta], feed_dict = {x: ex, y: ey})
            blad_suma += blad;

        print ('Cykl ', cykl, ' z ', ilosc_cykli, ' blad to ', blad_suma)

    poprawnie = tf.equal(tf.argmax(wynik, 1), tf.argmax(y, 1))
    trafnosc_odpowiedzi = tf.reduce_mean(tf.cast(poprawnie, 'float'))

    print('Prawdopodobienstwo trafienia 0..1 : ', trafnosc_odpowiedzi.eval(feed_dict={x: mnist.test.images, y: mnist.test.labels}))


# print (mnist.test.images[0])
# print (mnist.test.labels[0])
trenuj(x)

import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn import preprocessing

from ML import MakeVar as mv

varnum = 2
df = pd.read_excel('BankruptcyStock(TestRefine).xls')
xy = df.as_matrix().transpose()

x_dataTest = mv.MakeVar1(xy,varnum)
y_dataTest = xy[-1].astype(np.float32)             # 1행 6열
W = tf.Variable(tf.random_uniform([1, len(x_dataTest[0][:-varnum])]))
score = 0

with tf.Session() as sess:
    saver = tf.train.Saver()
    saver.restore(sess, "./model.ckpt")

    X = tf.placeholder(tf.float32, shape=(None, None))
    h = tf.matmul(sess.run(W), X)
    hypothesis = tf.div(1., 1. + tf.exp(-h))  # exp(-h) = e ** -h. e는 자연상수

    for j in range(0, len(x_dataTest[0][0])):
        Testlist = []
        for varlist in range(0, varnum + 1):
            Testlist.append([x_dataTest[6][varlist][j]])
        if ((sess.run(hypothesis, feed_dict={X: Testlist}) > 0.66)[0][0] == y_dataTest[j]):
            score = score + 1

    print('적중률: ', round((score / len(x_dataTest[0][0])) * 100, 2), '%')

sess.close()

'''
x_data = mv.MakeVar1(xy, 3)
for i in range(0,len(x_data)):
    for i in range(0,1):
        X = tf.placeholder(tf.float32)
        Y = tf.placeholder(tf.float32)
        W = tf.Variable(tf.random_uniform([1, len(x_data[0][:-3])], -1.0, 1.0))
        h = tf.matmul(W, X)

        hypothesis = tf.div(1., 1. + tf.exp(-h))  # exp(-h) = e ** -h. e는 자연상수
        cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) * tf.log(1 - hypothesis))
        rate = tf.Variable(0.01)
        optimizer = tf.train.GradientDescentOptimizer(rate)
        train = optimizer.minimize(cost)
        init = tf.global_variables_initializer()
        sess = tf.Session()
        sess.run(init)
        tf.summary.scalar('cost',cost)
        merged_summary_op = tf.summary.merge_all


        for step in range(3001):
            sess.run(train, feed_dict={X: x_data[i][:-3], Y: y_data})
            if step % 20 == 0:
                sess.run(cost, feed_dict={X: x_data[i][:-3], Y: y_data}), sess.run(W)
                #print(step, sess.run(cost, feed_dict={X: x_data[i][:-2], Y: y_data}), sess.run(W))
        print('-----------------------------------------')
        # 결과가 0 또는 1로 계산되는 것이 아니라 0과 1 사이의 값으로 나오기 때문에 True/False는 직접 판단
        df = pd.read_excel('BankruptcyStock(TestRefine).xls')
        xy = df.as_matrix().transpose()
        x_dataTest = mv.MakeVar1(xy,3)
        y_dataTest = xy[-1].astype(np.float32)             # 1행 6열
        score = 0
        for j in range(0,len(x_dataTest[0][0])):
            #print('[', x_dataTest[i][0][j], x_dataTest[i][1][j], x_dataTest[i][2][j], y_dataTest[j],']: ',sess.run(hypothesis, feed_dict={X: [[x_dataTest[i][0][j]], [x_dataTest[i][1][j]], [x_dataTest[i][2][j]] ]}) > 0.7)
            Testlist = []
            for varlist in range(0,3+1):
                Testlist.append([x_dataTest[i][varlist][j]])
            #print(Testlist,' : ' ,sess.run(hypothesis,feed_dict={X: Testlist}) > 0.7)
            if ((sess.run(hypothesis,feed_dict={X: Testlist}) > 0.6)[0][0] == y_dataTest[j]):
                score = score + 1

        for printvar in range(1,3+1):
            print('변수',printvar,x_dataTitle[x_data[i][-printvar]])
        print('적중률: ', round((score/len(x_dataTest[0][0]))*100,2),'%')

        sess.close()
'''
from PIL import Image
import numpy as np
import os
import random
import tensorflow as tf
import time
import py_spider.get_code.vaLemission_control as mc
import io
import base64


class CaptchaTrain:
    '''训练Cnn'''
    MAX_CAPTCHA = mc.MAX_CAPTCHA
    VERIFY_CODES = mc.VERIFY_CODES
    CHAR_SET_LEN = len(VERIFY_CODES)
    IMAGE_HEIGHT = 60
    IMAGE_WIDTH = 160
    X = tf.placeholder(tf.float32, [None, IMAGE_HEIGHT * IMAGE_WIDTH])
    Y = tf.placeholder(tf.float32, [None, MAX_CAPTCHA * CHAR_SET_LEN])
    keep_prob = tf.placeholder(tf.float32)  # dropout
    imageMap={}
    imageList=[]
    #        filePath = "F:/verifies/"

    def __init__(self,filePath,createModel,saveModel,level = 0.9,restore=False,saveTime=False):
        self.filePath=filePath
        self.createModel=createModel
        self.saveModel = saveModel
        self.level=level
        self.restore=restore
        self.saveTime=saveTime
        isExists = os.path.exists(self.saveModel+'Model/')
        if not isExists:
            os.makedirs(self.saveModel+'Model/')

    # 把彩色图像转为灰度图像（色彩对识别验证码没有什么用）
    def convert2gray(self,img):
        if len(img.shape) > 2:
            #gray = np.mean(img, -1)
            # 上面的转法较快，正规转法如下
            r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
            gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
            return gray
        else:
            return img

    # 把字符串转化为向量
    def text2vec(self,text):
        vector = np.zeros(self.MAX_CAPTCHA * self.CHAR_SET_LEN)
        if len(text) < self.MAX_CAPTCHA:
            i = self.MAX_CAPTCHA - len(text)
            text += "_" * i
        def char2pos(c):
            return self.VERIFY_CODES.index(c)
        for i, c in enumerate(text):
            idx = i * self.CHAR_SET_LEN + char2pos(c)
            vector[idx] = 1
        return vector

    # 向量转回文本
    def vec2text(self,vec):
        char_pos = vec.nonzero()[0]
        text = []
        for i, c in enumerate(char_pos):
            char_at_pos = i  # c/63
            char_idx = c % self.CHAR_SET_LEN
            text.append(self.VERIFY_CODES[char_idx])
        return "".join(text)

    #读取本地图片到map里面
    def readImg2Map(self):
        pathDir = os.listdir(self.filePath)
        for allDir in pathDir:
            tempArr = []
            text = allDir.split('_')
            fileName = self.filePath + allDir
            self.imageMap[fileName] = text[0]
            self.imageList.append(fileName)

    #读取内存map排序
    def next_batch(self,batch_size=64):
        batch_x = np.zeros([batch_size, self.IMAGE_HEIGHT * self.IMAGE_WIDTH])
        batch_y = np.zeros([batch_size, self.MAX_CAPTCHA * self.CHAR_SET_LEN])

        list1 = random.sample(self.imageList,batch_size)
        for index, item in enumerate(list1):
            batch_x[index, :] = self.getImage(item)
            #print(self.imageMap[item])
            batch_y[index, :] = self.text2vec(self.imageMap[item].lower())
        return batch_x, batch_y
        ####################################################################
        #map = PicGet.getListMap(batch_size)
        #index=0
        #for k, v in map.items():
            #batch_x[index, :] = self.getImage(io.BytesIO(base64.b64decode(k)))
                # print(self.imageMap[item])
            #batch_y[index, :] = self.text2vec(v.lower())
            #index=index+1
        #return batch_x, batch_y
        ####################################################################

    # 读取本地图片
    def getImage(self,fileName):
        imgArr = []
        img = np.array(Image.open(fileName).convert('L').resize((self.IMAGE_WIDTH, self.IMAGE_HEIGHT), Image.ANTIALIAS))
        rows, cols = img.shape
        for i in range(rows):
            for j in range(cols):
                imgArr.append((img[i, j] - 128) / 128)
        return imgArr

    # 生成一个训练batch
    def get_next_batch(self,batch_size=64):
        batch_x = np.zeros([batch_size, self.IMAGE_HEIGHT * self.IMAGE_WIDTH])
        batch_y = np.zeros([batch_size, self.MAX_CAPTCHA * self.CHAR_SET_LEN])

        # 构造训练值
        i = 0
        pathDir = os.listdir(self.filePath)
        for allDir in pathDir:
            tempArr = []
            text = allDir.split('_')
            fileName = self.filePath + allDir
            imgArr = self.getImage(fileName)
            batch_x[i, :] = imgArr
            batch_y[i, :] = self.text2vec(text[0])
            i = i + 1
            if i == 64:
                break
        return batch_x, batch_y
        ####################################################################

    #定义神经网络
    # 定义CNN
    def crack_captcha_cnn(self,w_alpha=0.01, b_alpha=0.1):
        x = tf.reshape(self.X, shape=[-1, self.IMAGE_HEIGHT, self.IMAGE_WIDTH, 1])

        # 3 conv layer
        self.w_c1 = tf.Variable(w_alpha * tf.random_normal([3, 3, 1, 32]))#卷积核高度，卷积核宽度，图像通道数，卷积核个数
        self.b_c1 = tf.Variable(b_alpha * tf.random_normal([32]))

        conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, self.w_c1, strides=[1, 1, 1, 1], padding='SAME'), self.b_c1))
        conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        #conv1 = tf.nn.dropout(conv1, self.keep_prob)

        self.w_c2 = tf.Variable(w_alpha * tf.random_normal([3, 3, 32, 64]))
        self.b_c2 = tf.Variable(b_alpha * tf.random_normal([64]))
        conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, self.w_c2, strides=[1, 1, 1, 1], padding='SAME'), self.b_c2))
        conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        #conv2 = tf.nn.dropout(conv2, self.keep_prob)

        self.w_c3 = tf.Variable(w_alpha * tf.random_normal([3, 3, 64, 128]))
        self.b_c3 = tf.Variable(b_alpha * tf.random_normal([128]))
        conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, self.w_c3, strides=[1, 1, 1, 1], padding='SAME'), self.b_c3))
        #conv3 = tf.nn.dropout(conv3, self.keep_prob)

        self.w_c4 = tf.Variable(w_alpha * tf.random_normal([3, 3, 128, 128]))
        self.b_c4 = tf.Variable(b_alpha * tf.random_normal([128]))
        conv4 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv3, self.w_c4, strides=[1, 1, 1, 1], padding='SAME'), self.b_c4))
        #conv4 = tf.nn.dropout(conv4, self.keep_prob)

        self.w_c5 = tf.Variable(w_alpha * tf.random_normal([3, 3, 128, 256]))
        self.b_c5 = tf.Variable(b_alpha * tf.random_normal([256]))
        conv5 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv4, self.w_c5, strides=[1, 1, 1, 1], padding='SAME'), self.b_c5))
        conv5 = tf.nn.max_pool(conv5, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        #conv5 = tf.nn.dropout(conv5, self.keep_prob)
        if self.restore:
            conv5_sg = tf.stop_gradient(conv5)  # It's an identity function

        self.w_c6 = tf.Variable(w_alpha * tf.random_normal([3, 3, 256, 512]))
        self.b_c6 = tf.Variable(b_alpha * tf.random_normal([512]))
        conv6 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv5, self.w_c6, strides=[1, 1, 1, 1], padding='SAME'), self.b_c6))
        conv6 = tf.nn.max_pool(conv6, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

        # Fully connected layer
        self.w_d = tf.Variable(w_alpha * tf.random_normal([4 * 10 * 512, 1024]))
        self.b_d = tf.Variable(b_alpha * tf.random_normal([1024]))
        dense = tf.reshape(conv6, [-1, self.w_d.get_shape().as_list()[0]])
        dense = tf.nn.relu(tf.add(tf.matmul(dense, self.w_d), self.b_d))
        dense = tf.nn.dropout(dense, self.keep_prob)

        self.w_d1 = tf.Variable(w_alpha * tf.random_normal([1024, 1024]))
        self.b_d1 = tf.Variable(b_alpha * tf.random_normal([1024]))
        dense1 = tf.nn.relu(tf.add(tf.matmul(dense, self.w_d1), self.b_d1))
        #dense1 = tf.nn.dropout(dense1, self.keep_prob)

        w_out = tf.Variable(w_alpha * tf.random_normal([1024, self.MAX_CAPTCHA * self.CHAR_SET_LEN]))
        b_out = tf.Variable(b_alpha * tf.random_normal([self.MAX_CAPTCHA * self.CHAR_SET_LEN]))
        out = tf.add(tf.matmul(dense1, w_out), b_out)
        # out = tf.nn.softmax(out)
        return out

    def del_files(self,path):
        for root, dirs, files in os.walk(path):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except:
                    continue

    def con_files(self,path):
        ls = os.listdir(path)
        count = 0
        for i in ls:
            if os.path.isfile(os.path.join(path, i)):
                count += 1
        return count

    # 训练
    def train_crack_captcha_cnn(self):
        output = self.crack_captcha_cnn()
        loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=self.Y))
        optimizer = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(loss)#learning_rate=0.001
        predict = tf.reshape(output, [-1, self.MAX_CAPTCHA, self.CHAR_SET_LEN])
        max_idx_p = tf.argmax(predict, 2)
        max_idx_l = tf.argmax(tf.reshape(self.Y, [-1, self.MAX_CAPTCHA, self.CHAR_SET_LEN]), 2)
        correct_pred = tf.equal(max_idx_p, max_idx_l)
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
        saver = tf.train.Saver([self.w_c1,self.b_c1,self.w_c2,self.b_c2,self.w_c3,self.b_c3,self.w_c4,self.b_c4,self.w_c5,self.b_c5,self.w_d,self.b_d,self.w_d1,self.b_d1])
        saverAll=tf.train.Saver()
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        with tf.Session(config=config) as sess:
            if self.restore:
                sess.run(tf.global_variables_initializer())
                saver.restore(sess, self.createModel + 'model/model.ckpt')
            else:
                saverAll.restore(sess, self.createModel + 'model/model.ckpt')
            step = 0
            self.readImg2Map()
            while True:
                batch_x, batch_y = self.next_batch(32)
                if step % mc.modelSaveTime == 0 and step!=0 :
                    batch_x_test, batch_y_test = batch_x, batch_y
                    acc = sess.run(accuracy, feed_dict={self.X: batch_x_test, self.Y: batch_y_test, self.keep_prob: 1.})
                    print("第 %d 批次,acc准确率是 %f " % (step, acc))
                    if acc>0.92 or step >10000:
                        saverAll.save(sess, self.saveModel + 'Model/model.ckpt')
                        # break  # 可加可不加
                    saverAll.save(sess, self.saveModel+'Model/model.ckpt')
                _, loss_ = sess.run([optimizer, loss], feed_dict={self.X: batch_x, self.Y: batch_y, self.keep_prob: 0.5})
                print("第 %d 批次,loss值是 %f " % (step, loss_))
                if self.saveTime :
                    saverAll.save(sess, self.saveModel + 'Model/model.ckpt')
                step += 1

if __name__=='__main__':
    #cnn最原始模型 level1混合训练第一版 level2混合训练第二版(训练次数加大)
    #第一个参数为路径，第二个参数为原始模型，第三个参数保存到什么位置，第四个参数模型的精度，第五参数是用现有模型训练还是初创参数，第六个参数是不是每次调参都保存
    #captchaTrain=CaptchaTrain(mc.yanZhengMaPath,mc.modelSaveName+"4",mc.modelSaveName+"Deep",0.01,True,False)
    captchaTrain = CaptchaTrain(mc.yanZhengMaPath, "levelDeep4", "cw", 0.9, False, False)
    captchaTrain.train_crack_captcha_cnn()
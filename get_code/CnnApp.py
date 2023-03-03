import numpy as np
import tensorflow as tf
import time
import json
import base64
import asyncio
from aiohttp import web
from io import BytesIO
from PIL import Image


class CaptchaPredit:
    '''训练Cnn'''
    MAX_CAPTCHA = 6
    VERIFY_CODES = "abcdefghijklmnopqrstuvwxyz0123456789_"
    CHAR_SET_LEN = len(VERIFY_CODES)
    IMAGE_HEIGHT = 60
    IMAGE_WIDTH = 160

    def __init__(self, model):
        self.X = tf.placeholder(tf.float32, [None, self.IMAGE_HEIGHT * self.IMAGE_WIDTH])
        self.Y = tf.placeholder(tf.float32, [None, self.MAX_CAPTCHA * self.CHAR_SET_LEN])
        self.keep_prob = tf.placeholder(tf.float32)  # dropout
        self.model = model
        self.sess = tf.Session()
        self.output = self.crack_captcha_cnn()
        self.saver = tf.train.Saver()
        # self.saver.restore(self.sess, './model.ckpt')
        self.saver.restore(self.sess, self.model + 'Model/model.ckpt')
        self.predict = tf.argmax(tf.reshape(self.output, [-1, self.MAX_CAPTCHA, self.CHAR_SET_LEN]), 2)

    # 把彩色图像转为灰度图像（色彩对识别验证码没有什么用）
    def convert2gray(self, img):
        if len(img.shape) > 2:
            gray = np.mean(img, -1)
            # 上面的转法较快，正规转法如下
            # r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
            # gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
            return gray
        else:
            return img

    # 把字符串转化为向量
    def text2vec(self, text):
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
    def vec2text(self, vec):
        char_pos = vec.nonzero()[0]
        text = []
        for i, c in enumerate(char_pos):
            char_at_pos = i  # c/63
            char_idx = c % self.CHAR_SET_LEN
            text.append(self.VERIFY_CODES[char_idx])
        return "".join(text)

    # 读取本地图片
    def getImage(self, image_content):
        imgArr = []
        im = Image.open(BytesIO(image_content))
        # img = np.array(Image.open(fileName).convert('L'))
        img = np.array(im.convert('L').resize((self.IMAGE_WIDTH, self.IMAGE_HEIGHT), Image.ANTIALIAS))
        rows, cols = img.shape
        for i in range(rows):
            for j in range(cols):
                imgArr.append((img[i, j] - 128) / 128)
        return imgArr

    # 定义神经网络
    # 定义CNN
    def crack_captcha_cnn(self, w_alpha=0.01, b_alpha=0.1):
        x = tf.reshape(self.X, shape=[-1, self.IMAGE_HEIGHT, self.IMAGE_WIDTH, 1])

        # 3 conv layer
        self.w_c1 = tf.Variable(w_alpha * tf.random_normal([3, 3, 1, 32]))
        self.b_c1 = tf.Variable(b_alpha * tf.random_normal([32]))
        conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, self.w_c1, strides=[1, 1, 1, 1], padding='SAME'), self.b_c1))
        conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # conv1 = tf.nn.dropout(conv1, self.keep_prob)

        self.w_c2 = tf.Variable(w_alpha * tf.random_normal([3, 3, 32, 64]))
        self.b_c2 = tf.Variable(b_alpha * tf.random_normal([64]))
        conv2 = tf.nn.relu(
            tf.nn.bias_add(tf.nn.conv2d(conv1, self.w_c2, strides=[1, 1, 1, 1], padding='SAME'), self.b_c2))
        conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # conv2 = tf.nn.dropout(conv2, self.keep_prob)

        self.w_c3 = tf.Variable(w_alpha * tf.random_normal([3, 3, 64, 128]))
        self.b_c3 = tf.Variable(b_alpha * tf.random_normal([128]))
        conv3 = tf.nn.relu(
            tf.nn.bias_add(tf.nn.conv2d(conv2, self.w_c3, strides=[1, 1, 1, 1], padding='SAME'), self.b_c3))
        # conv3 = tf.nn.dropout(conv3, self.keep_prob)

        self.w_c4 = tf.Variable(w_alpha * tf.random_normal([3, 3, 128, 128]))
        self.b_c4 = tf.Variable(b_alpha * tf.random_normal([128]))
        conv4 = tf.nn.relu(
            tf.nn.bias_add(tf.nn.conv2d(conv3, self.w_c4, strides=[1, 1, 1, 1], padding='SAME'), self.b_c4))
        # conv4 = tf.nn.dropout(conv4, self.keep_prob)

        self.w_c5 = tf.Variable(w_alpha * tf.random_normal([3, 3, 128, 256]))
        self.b_c5 = tf.Variable(b_alpha * tf.random_normal([256]))
        conv5 = tf.nn.relu(
            tf.nn.bias_add(tf.nn.conv2d(conv4, self.w_c5, strides=[1, 1, 1, 1], padding='SAME'), self.b_c5))
        conv5 = tf.nn.max_pool(conv5, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # conv5 = tf.nn.dropout(conv5, self.keep_prob)

        self.w_c6 = tf.Variable(w_alpha * tf.random_normal([3, 3, 256, 512]))
        self.b_c6 = tf.Variable(b_alpha * tf.random_normal([512]))
        conv6 = tf.nn.relu(
            tf.nn.bias_add(tf.nn.conv2d(conv5, self.w_c6, strides=[1, 1, 1, 1], padding='SAME'), self.b_c6))
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
        # dense1 = tf.nn.dropout(dense1, self.keep_prob)

        w_out = tf.Variable(w_alpha * tf.random_normal([1024, self.MAX_CAPTCHA * self.CHAR_SET_LEN]))
        b_out = tf.Variable(b_alpha * tf.random_normal([self.MAX_CAPTCHA * self.CHAR_SET_LEN]))
        out = tf.add(tf.matmul(dense1, w_out), b_out)
        # out = tf.nn.softmax(out)
        return out

    def crack_captcha(self, captcha_image):
        text_list = self.sess.run(self.predict, feed_dict={self.X: [captcha_image], self.keep_prob: 1})
        text = text_list[0].tolist()
        vector = np.zeros(self.MAX_CAPTCHA * self.CHAR_SET_LEN)
        i = 0
        for n in text:
            vector[i * self.CHAR_SET_LEN + n] = 1
            i += 1
        return self.vec2text(vector)

    def predictCaptcha(self, fileName):
        image = self.getImage(fileName)
        predict_text = self.crack_captcha(image)[:-1].upper()
        return predict_text

    def cnnPredict(self, img1):
        imgArr = []
        img = np.array(img1.convert('L').resize((self.IMAGE_WIDTH, self.IMAGE_HEIGHT), Image.ANTIALIAS))
        rows, cols = img.shape
        for i in range(rows):
            for j in range(cols):
                imgArr.append((img[i, j] - 128) / 128)
        predict_text = self.crack_captcha(imgArr)
        return predict_text


async def zqsx(request):
    info = await request.text()
    info = json.loads(info)
    img = info['img']
    # img = info.split('=')[1]+'=='
    # print(img)
    img_byte = base64.b64decode(img)
    v = captchaTrain.predictCaptcha(img_byte)
    print(v)
    return web.Response(body='{}'.format(v))


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('POST', '/zqsx', zqsx)
    await loop.create_server(app.make_handler(), '127.0.0.1', 8009)


if __name__ == '__main__':
    import os
    only_path = os.path.join(os.getcwd()+'\model', 'zhixingModel').replace('Model', '')
    # only_path = os.path.join(os.getcwd()+'\model', 'shanghaiModel').replace('Model', '')
    # only_path = os.path.join(os.getcwd()+'\model', 'beijingModel').replace('Model', '')
    # only_path = os.path.join(os.getcwd()+'\model', 'dt1Model').replace('Model', '')
    # only_path = os.path.join(os.getcwd()+'\model', 'susongModel').replace('Model', '')
    captchaTrain = CaptchaPredit(only_path)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
    # beizhixing: 4,789,408
    # zhongbenanjian:1,040,958
    # shixinbeizhixing:8,023,019
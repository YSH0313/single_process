const { formatPrint } = require('./utils');
const { genCookie } = require('./encrypt');

const express = require('express');
const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.json({limit:'100mb'}));
app.use(bodyParser.urlencoded({ limit:'100mb', extended: true }));
var multipart = require('connect-multiparty');
var multipartMiddleware = multipart();
/**************************************生成 cookie **************************************/
app.post('/api/cookie', multipartMiddleware, function (req, res) {
    let link = req.body.link
      , html = req.body.html
      , cookies = req.body.cookies;
    if (!html || !cookies) {
        res.json({
            code: 404,
            errorMsg: 'param error',
            data: null
        });
    } else {
        try {
            result = genCookie(html, cookies, link);
            res.json({
                code: 200,
                errorMsg: 'success',
                data: result
            })
        } catch (e) {
            console.log(e);
            res.json({
                code: 500,
                errorMsg: 'internal error',
                data: null
            })
        }
    }
});
/**************************************启动服务**************************************/
const server = app.listen(7888, function() {
    let host = server.address().address;
    let port = server.address().port;
    console.log(formatPrint(
        'INFO',
        `瑞数加密服务启动, 监听地址为: http://${host}:${port}`
        )
    )
});

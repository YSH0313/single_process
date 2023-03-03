function decryptByDES(_0x3282ec, _0x3dcce1) {
    var CryptoJS = require("crypto-js");
    var _0x456351 = CryptoJS['enc']['Utf8']["parse"](_0x3dcce1);
    var _0x3c5437 = CryptoJS["DES"]["decrypt"]({
        'ciphertext': CryptoJS["enc"]["Base64"]["parse"](_0x3282ec)
    }, _0x456351, {
        'mode': CryptoJS["mode"]["ECB"],
        'padding': CryptoJS["pad"]['Pkcs7']
    });
    return _0x3c5437['toString'](CryptoJS["enc"]["Utf8"]);
}

function get_url(str_data) {
    var code = decryptByDES(str_data, 'Ctpsp@884*');
    console.log(code)
    return code
}get_url("L0j+JvbeVM0svSpjIwXdE7yTu78wiEsz1kF33NxVroXg6lZUaOH6Bx/Zl/61RnOfoar9nIDj2hSESOkGU1YwM8ddEuuoTg5uPsqQ9/SuNds=")


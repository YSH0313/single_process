const jsdom = require('jsdom');
const { JSDOM } = jsdom;
/************************************************** 获取 html源码 **************************************************/

process.on('uncaughtException', (e) => {
  console.log(e);
  // console.log(e);
});


// const window = (new JSDOM(``, { runScripts: "dangerously" , pretendToBeVisual: true})).window;
// window.onModulesLoaded = () => {
//   console.log("ready to roll!");
// };
// //渲染js执行后的结果
// const dom = new JSDOM(``, { runScripts: "dangerously" , pretendToBeVisual: true});
// JSDOM.fromURL('https://www.bfa.edu.cn/guoziban/tzgg/48.htm', {runScripts: 'dangerously', pretendToBeVisual: true}).then((dom) => {
//   console.log(dom.serialize());
// });


JSDOM.fromURL('https://www.bfa.edu.cn/guoziban/tzgg/48.htm', {runScripts: 'dangerously', pretendToBeVisual: true}).then(dom => {
  console.log(dom.serialize().cookies);
});


// function genCookie(ht, link) {
//     var options = {
//         referrer: link,
//         userAgent: "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
//         // resources: "usable",
//         runScripts: "dangerously",
//         url: link,
//         beforeParse(window) {
//             window.js = 'none';
//             window.setInterval = function (s, b) {
//                 return 1
//             };
//             window.setTimeout = function (s, b) {
//                 return 1
//             };
//         },
//         // virtualConsole: new jsdom.VirtualConsole(),
//         cookieJar: new jsdom.CookieJar(),
//     };
//     // options.cookieJar.setCookie(ck, link, cp);
//     function cp(val) {
//         if (val) {
//         }
//     }
//     const dom = (new JSDOM(ht, options))
//     return dom.serialize()
//     // const window = dom.window;
//     // documentElement = window.document.body;
//     // return documentElement
// }
//
// module.exports = {
//     genCookie
// };
//
//
// function Base64() {
//
//     // private property
//     _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
//
//     // public method for encoding
//     this.encode = function (input) {
//         var output = "";
//         var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
//         var i = 0;
//         input = _utf8_encode(input);
//         while (i < input.length) {
//             chr1 = input.charCodeAt(i++);
//             chr2 = input.charCodeAt(i++);
//             chr3 = input.charCodeAt(i++);
//             enc1 = chr1 >> 2;
//             enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
//             enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
//             enc4 = chr3 & 63;
//             if (isNaN(chr2)) {
//                 enc3 = enc4 = 64;
//             } else if (isNaN(chr3)) {
//                 enc4 = 64;
//             }
//             output = output +
//             _keyStr.charAt(enc1) + _keyStr.charAt(enc2) +
//             _keyStr.charAt(enc3) + _keyStr.charAt(enc4);
//         }
//         return output;
//     }
//
//     // public method for decoding
//     this.decode = function (input) {
//         var output = "";
//         var chr1, chr2, chr3;
//         var enc1, enc2, enc3, enc4;
//         var i = 0;
//         input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
//         while (i < input.length) {
//             enc1 = _keyStr.indexOf(input.charAt(i++));
//             enc2 = _keyStr.indexOf(input.charAt(i++));
//             enc3 = _keyStr.indexOf(input.charAt(i++));
//             enc4 = _keyStr.indexOf(input.charAt(i++));
//             chr1 = (enc1 << 2) | (enc2 >> 4);
//             chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
//             chr3 = ((enc3 & 3) << 6) | enc4;
//             output = output + String.fromCharCode(chr1);
//             if (enc3 != 64) {
//                 output = output + String.fromCharCode(chr2);
//             }
//             if (enc4 != 64) {
//                 output = output + String.fromCharCode(chr3);
//             }
//         }
//         output = _utf8_decode(output);
//         return output;
//     }
//
//     // private method for UTF-8 encoding
//     _utf8_encode = function (string) {
//         string = string.replace(/\r\n/g,"\n");
//         var utftext = "";
//         for (var n = 0; n < string.length; n++) {
//             var c = string.charCodeAt(n);
//             if (c < 128) {
//                 utftext += String.fromCharCode(c);
//             } else if((c > 127) && (c < 2048)) {
//                 utftext += String.fromCharCode((c >> 6) | 192);
//                 utftext += String.fromCharCode((c & 63) | 128);
//             } else {
//                 utftext += String.fromCharCode((c >> 12) | 224);
//                 utftext += String.fromCharCode(((c >> 6) & 63) | 128);
//                 utftext += String.fromCharCode((c & 63) | 128);
//             }
//
//         }
//         return utftext;
//     }
//
//     // private method for UTF-8 decoding
//     _utf8_decode = function (utftext) {
//         var string = "";
//         var i = 0;
//         var c = c1 = c2 = 0;
//         while ( i < utftext.length ) {
//             c = utftext.charCodeAt(i);
//             if (c < 128) {
//                 string += String.fromCharCode(c);
//                 i++;
//             } else if((c > 191) && (c < 224)) {
//                 c2 = utftext.charCodeAt(i+1);
//                 string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
//                 i += 2;
//             } else {
//                 c2 = utftext.charCodeAt(i+1);
//                 c3 = utftext.charCodeAt(i+2);
//                 string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
//                 i += 3;
//             }
//         }
//         return string;
//     }
// }
//
// var base = new Base64()
// var params = process.argv.splice(2)
// // console.log(params)
// var html = base.decode(params[0])
// var data = genCookie(html, params[1])
// console.log(data)

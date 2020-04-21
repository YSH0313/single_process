
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
window = dom.window;
document = window.document;
XMLHttpRequest = window.XMLHttpRequest;

function a(data) {
    var b = data;
    console.log(b);
    return b
}

// def tes(self):
//     import execjs
//     with open('D:\\work\\single_process\\js\\tes.js', 'r', encoding='utf-8') as f:
//         js = f.read()
//     ct = execjs.compile(js, cwd=r'C:\Users\ysh\AppData\Roaming\npm\node_modules')
//     print(ct.call('a', '1'))
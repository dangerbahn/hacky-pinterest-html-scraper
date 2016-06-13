'use strict'
var fs = require('fs');
var cofs = require('co-fs');
var express = require('express');
var wrap = require('co-express');
var http = require('http');
var https = require('https');
var request = require('request');
var privateKey  = fs.readFileSync('key.pem', 'utf8');
var certificate = fs.readFileSync('key-cert.pem', 'utf8');

var credentials = {key: privateKey, cert: certificate};




var app = express();

app.get('/', wrap(function* (req, res) {
  // var packageContents = yield cofs.readFile('./package.json', 'utf8');
  // res.send(packageContents);
  var test = yield getBoards()
  res.send(test);
}));
app.get('/oauth', wrap(function* (req, res) {
  // var packageContents = yield cofs.readFile('./package.json', 'utf8');
  // res.send(packageContents);
  res.send(req,res);
}));




// your express configuration here

var httpServer = http.createServer(app);
var httpsServer = https.createServer(credentials, app);

httpServer.listen(8080);
httpsServer.listen(8000);

//
// https://api.pinterest.com/v1/me/pins/?
//     access_token=<YOUR-ACCESS-TOKEN>
//     &fields=id,creator,note
//     &limit=1
const getBoards = function *() {
    let req = {
      uri: 'https://api.pinterest.com/v1/boards/heatherhortone/baby-select-diapering-wall/',
      method: 'GET',
      gzip: true,
      qs: {access_token: 'AYkm2xFnx5dyURXDfJWzFjSCejJbFFbTdZaAsdxDKRNMy-AsQQAAAAA'},
      headers : { 'access_token': 'AYkm2xFnx5dyURXDfJWzFjSCejJbFFbTdZaAsdxDKRNMy-AsQQAAAAA' },
      timeout: 10000,
      json: true,
      jar: false
    }

    return new Promise ( function (resolve, reject) {
        request(req, (err, res, body) => {
            if (err) {
                reject(err)
            }
resolve(res, body)

        })
    })
}

const callRedsky = function *(tcin) {
    let req = {
      uri: 'https://www.tgtappdata.com/v1/products/pdp/TCIN/' + tcin,
      method: 'GET',
      gzip: true,
      qs: {key: '6bf34d7581ae95886036b732'},
      headers : { 'X-REQUIRE-STORE-INFO': true },
      timeout: 10000,
      json: true,
      jar: false
    }

    return new Promise ( function (resolve, reject) {
        request(req, (err, res, body) => {
            if (err) {
                reject(err)
            }

            if (res.statusCode === 200) {
                var resp = body[0] ? body[0] : body;
                resolve(resp)
            } else {
                resolve({"upc": "not found", "tcin": "not found", "DPCI": "not found"})
            }
        })
    })
}

const express = require('express');
const Device = require('../models/Device');

module.exports = {
    doGetDevices : function(req, res, next){
        const room_number = req.params.roomNumber;
        const data = {
            'room_number' : room_number
        }

        console.log('search device list in #room : ', room_number);
        Device.getDevices(data).then((result)=>{
            res.send(result);
        })
    }
    ,
    OnDevice : function(req, res, next){
        const data = {
            'device_number' : req.body.device_number
        }
        
        var fs = require('fs');
        var openApiURL = 'http://aiopen.etri.re.kr:8000/WiseASR/Recognition';
        var accessKey = '0daad576-d02b-434e-a5ea-3db5adf90b74';
        var languageCode = 'korean';
        var audioFilePath = 'C:\\Users\\multicampus\\Downloads\\KOR_F_RM0769FLJH0325\\KOR_F_RM0769FLJH0325.pcm';
        var audioData;

        var audioData = fs.readFileSync(audioFilePath);

        var requestJson = {
            'access_key': accessKey,
            'argument': {
                'language_code': languageCode,
                'audio': audioData.toString('base64')
            }
        };

        var request = require('request');
        var options = {
            url: openApiURL,
            body: JSON.stringify(requestJson),
            headers: {'Content-Type':'application/json; charset=UTF-8'}
        };
        request.post(options, function (error, response, body) {
            console.log('responseCode = ' + response.statusCode);
            console.log('responseBody = ' + body);
        });
        
        console.log('turn on #device : ', req.body.device_number);
        Device.onDevice(data).then((result)=>{
            res.send(result);
        });
    },
    OffDevice : function(req, res, next){
        const data = {
            'device_number' : req.body.device_number
        }
        // ROS device off 메세지 전송
        req.io.emit('msg', 'device off!');
        
        console.log('turn off #device : ', req.body.device_number);
        Device.offDevice(data).then((result)=>{
            res.send(result);
        });
    }
}
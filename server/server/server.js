
// Websocket 서버 구동을 위한 서버 코드입니다.

// 노드 로직 순서

const path = require('path');
const express = require('express');

const employee_service = require('./models/Employee');
const device_service = require('./models/Device');
const room_service = require('./models/Room');
// client 경로의 폴더를 지정해줍니다.
// const publicPath = path.join(__dirname, "/../client");
var app = express();

// const picPath = path.join(__dirname, "/../client");

// app.use(express.static(publicPath));

// 로직 1. WebSocket 서버, WebClient 통신 규약 정의
const server = require('http').createServer(app);
const io = require('socket.io')(server)


var fs = require('fs'); // required for file serving

// 로직 2. 포트번호 지정
const port = process.env.port || 12001

server.listen(port, () => {
    console.log(`listening on *:${port}`);
    require('dns').lookup(require('os').hostname(), function (err, add, fam) {
        console.log('addr: ' + add);
    })
});

const roomName = 'team';

io.on('connection', socket => {
    socket.join(roomName);
    console.log('connected');
    
    // Login
    socket.on('join', (data) => {
        employee_service.loginEmployee(data).then((result) => {
            // const loginCheck = 0
            if (result[0]) {
                // loginCheck = true
                // loginCheck = result[0]['employee_number']
                console.log(result[0]['employee_number']);
            }
            socket.emit('login', result)
        })
    })

    // GetEmployee
    socket.on('employee', (data) => {
        console.log(data);
        employee_service.getEmployee(data).then((result) => {
            socket.emit('putEmployee', result)
            console.log(result);
        })
    })

    // Vue -> Server

    // 가전기기 제어 (on/off)
    // data: {"room_name": , "device_name": , "on_off":}
    socket.on('deviceControl', async (data) => {
        console.log(data);
        const dataToROS = {};
        let device_result;
        //잘못된 데이터 입력시
        if(data.device_name === undefined || data.room_name === undefined || data.on_off === undefined || (data.on_off !== 'on' && data.on_off !== 'off' )){
            data = null;
        }
        console.log(data);
        if(data !== null){
            try{
                device_result = await device_service.searchDevice(data);
            }catch(err){
                console.log(err);
            }
            console.log(device_result);
            if(device_result !== null){
                dataToROS['arrival'] = {
                    'x' : device_result[0].x,
                    'y' : device_result[0].y,
                    'on_off' : data.on_off
                }
                
                console.log('dataToROS : ', dataToROS);
                // socket.to(roomName).emit('deviceControlToROS', dataToROS);
                io.emit('deviceControlToROS', dataToROS);
            }
        }
    })

    // 심부름
    //data = {"depart": , "stuff": , "arrival": }
    socket.on('stuffBring', async (data) => {
        //console.log('목적지로 이동')
        //console.log('x,y', data)
        // 음성 명령어에서 분리
        console.log(data);
        const command = {
            "depart" : data.depart,
            "stuff" : data.stuff,
            "arrival" : data.arrival,
        }
        const depart = {
            "name": command['depart']
        }
        const stuff = {
            "name": command['stuff']
        }
        const arrival = {
            "name": command['arrival']
        }
        
        const dataToROS = {};

        console.log('search start room by name : ', command['depart']);

        const depart_result = await room_service.getRoom(depart);
        const arrival_result = await room_service.getRoom(arrival);

        if(depart_result !== null && arrival_result !== null){
            dataToROS['depart'] = {"x" : depart_result[0].x, "y" : depart_result[0].y};
            dataToROS['stuff'] = stuff;
            dataToROS['arrival'] = {"x": arrival_result[0].x, "y" : arrival_result[0].y};

            socket.to(roomName).emit('stuffBringToROS', dataToROS);
        }
    })

    socket.on('env_msg_request_web', () => {
        // console.log('server get env msg req');
        socket.to(roomName).emit('env_msg_request_ros');
    }); 
    
    socket.on('env_msg_response_ros', (msg)=>{
        // console.log('ros response : ', msg);
        socket.to(roomName).emit('env_msg_response_web', msg);
    })

    socket.on('bot_status_request_web', ()=>{
        socket.to(roomName).emit('bot_status_request_ros');
    })

    socket.on('bot_status_response_ros', (msg)=>{
        socket.to(roomName).emit('bot_status_response_web', msg);
    })
    
    socket.on('employee_request_web', (msg)=>{
        socket.to(roomName).emit('employee_request_ros',msg);
    })

    socket.on('disconnect', () => {
        console.log('disconnected from server');
    });

    socket.on('jobDone', (msg)=>{
        console.log('작업하나 완료');
        io.emit('stuffBringCheck', msg);
    })

    // 전달받은 이미지를 jpg 파일로 저장
    socket.on('streaming', (message) => {
        socket.to(roomName).emit('sendStreaming', message);
        // console.log(message);
        buffer = Buffer.from(message, "base64");
        fs.writeFileSync(path.join(picPath, "/../client/cam.jpg"), buffer);
    });

})
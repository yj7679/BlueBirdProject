
// Websocket 서버 구동을 위한 서버 코드입니다.

// 노드 로직 순서

const path = require('path');
const express = require('express');

// const employee_service = require('./models/Employee');
// const device_service = require('./models/Device');
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
});

const roomName = 'team';

io.on('connection', socket => {
    socket.join(roomName);
    console.log('connected');
    // 로직 3. 사용자의 메시지 수신시 WebClient로 메시지 전달
    socket.on('env_msg', (message) => {
        console.log(message);
        socket.to(roomName).emit('envMsg', message);
    });

    // Vue -> Server

    // 기기 제어 On
    // data: {"room_name": , "device_name": }
    socket.on('deviceOn', (data) => {
        console.log(data, 'on');
    })

    // 기기 제어 Off
    // data: {"room_name": , "device_name": }
    socket.on('deviceOff', (data) => {
        console.log(data, 'off');
    })

    // 심부름
    //data = {"depart": , "stuff": , "arrival": }
    socket.on('stuffBring', (data) => {
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

        //console.log('search start room by name : ', command['depart']);
        room_service.getRoom(depart).then((result) => {

            console.log(result);
            
            if(result !== null){
                dataToROS['depart'] = { "x": result[0].x, "y": result[0].y }
                dataToROS['stuff'] = stuff
                room_service.getRoom(arrival).then((result) => {
                    var temp =  Object.values(JSON.parse(JSON.stringify(result)))
    
                    dataToROS['arrival'] = { "x": temp[0].x, "y": temp[0].y };
                    
                    console.log("ROS2(Client.py)로 보내는 데이터: ", dataToROS);
                    socket.to(roomName).emit('stuffBringToROS', dataToROS);
                })
            }
        })
    })

    socket.on('env_msg_request_web', () => {
        console.log('server get env msg req');
        socket.to(roomName).emit('env_msg_request_ros');
    }); 
    
    socket.on('env_msg_response_ros', (msg)=>{
        console.log('ros response : ', msg);
        socket.to(roomName).emit('env_msg_response_web', msg);
    })

    socket.on('bot_status_response', (msg)=>{
        console.log('bot status response : ', msg);
        
    })
    
    socket.on('disconnect', () => {
        console.log('disconnected from server');
    });

    // 전달받은 이미지를 jpg 파일로 저장
    socket.on('streaming', (message) => {
        socket.to(roomName).emit('sendStreaming', message);
        // console.log(message);
        buffer = Buffer.from(message, "base64");
        fs.writeFileSync(path.join(picPath, "/../client/cam.jpg"), buffer);
    });

})
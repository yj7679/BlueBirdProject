
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


    //data = ""
    socket.on('stuffBring', (data) => {
        console.log('목적지로 이동')
        //console.log('x,y', data)
        // 음성 명령어에서 분리
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
            //console.log(result)
            console.log("depart xy 뽑기")
            var temp =  Object.values(JSON.parse(JSON.stringify(result)))
            
            dataToROS['depart'] = { "x": temp[0].x, "y": temp[0].y }
            console.log(dataToROS['depart']);
        })

        //console.log('search destination room by name : ', command['arrival']);

        room_service.getRoom(arrival).then((result) => {
            var temp =  Object.values(JSON.parse(JSON.stringify(result)))
            //console.log(temp);
            dataToROS['arrival'] = { "x": temp[0].x, "y": temp[0].y }
            console.log(dataToROS['arrival']);
        })
        console.log("here..여기가 더빨리찍힘..어떻게 뽑은다음 데이터넣지..?")
        dataToROS['stuff'] = stuff.name
        //console.log(dataToROS['depart'])
       
        // // room_service.getRoom(where);
        // socket.to(roomName).emit('stuffBringToROS', result);
 
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
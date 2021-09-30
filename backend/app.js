const express = require('express');

const app = express();
<<<<<<< HEAD
const server = require('http').createServer(app);
const io = require('socket.io')(server);

const employeeRouter = require('./routes/employee');
const deviceRouter = require('./routes/device');
const cors = require('cors');

app.use(cors({
    origin: true,
    credentials: true
}))

app.set('port', 3000);

//요청 정보 확인
app.use(morgan('dev'));
//요청 cookie 파싱
app.use(cookieParser());

app.use((req, res, next)=>{
    req.io = io;
    next();
})
app.use('/device', deviceRouter);
app.use('/employee', employeeRouter);

io.on('connection', (socket)=>{
    console.log('connected socket');

    io.emit('usercount', io.engine.clientsCount);

    socket.on('env_msg',(msg)=>{
        console.log('env_msg : ', msg);
        io.emit('env_msg', msg);
        // socket.broadcast.emit('env_msg', msg);
    })

    socket.on('test', (data) => {
        console.log(data);
    })

    socket.on('disconnect',()=>{
        console.log('disconnected');
    })

})
=======
app.set('port', 3000);

const Router = require('./routes/router');
const deviceRouter = require('./routes/device');

app.use('/minimap', deviceRouter);
app.use('/', Router);
>>>>>>> parent of bb119f9 (Merge branch 'feature/astar' into 'develop')

app.listen(app.get('port'), ()=>{
    console.log('listen...port : ', app.get('port'));
});
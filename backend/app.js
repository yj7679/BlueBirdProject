const express = require('express');

const app = express();
app.set('port', 3000);

const Router = require('./routes/router');
const deviceRouter = require('./routes/device');

app.use('/minimap', deviceRouter);
app.use('/', Router);

app.listen(app.get('port'), ()=>{
    console.log('listen...port : ', app.get('port'));
});
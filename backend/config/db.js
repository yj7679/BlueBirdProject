const dotenv = require('dotenv');
const mysql = require('mysql');

dotenv.config();

const db = mysql.createConnection({
    host: 'localhost',
    port: '3306',
    user:'ssafy',
    password:'ssafy',
    database: 'bluebird'
    
})

db.connect(function(err){
    if(err){
        console.log('db connect err');
        console.log(err);
        throw err;
    }
    else{
        console.log('db connected');
    }
})

module.exports = db;
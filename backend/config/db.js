const dotenv = require('dotenv');
const mysql = require('mysql');

dotenv.config();

const db = mysql.createConnection({
    host:process.env.DB_HOST,
    port:process.env.DB_PORT,
    user:process.env.DB_USERNAME,
    password:process.env.DB_PASSWORD,
    database:process.env.DB_DATABASE
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
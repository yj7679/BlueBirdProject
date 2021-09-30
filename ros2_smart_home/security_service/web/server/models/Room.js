const db = require('../config/db');
const mybatisMapper = require('mybatis-mapper');
mybatisMapper.createMapper(['./mapper/room.xml']);

module.exports = {

    getRoom : function(name){
        console.log(name)
        const query = mybatisMapper.getStatement('room', 'searchRoomByRoomName', name);
        return new Promise((resolve, reject)=>{
            db.query(query, (err, result, fields)=>{
                if(err){
                    console.log(err);
                    reject(err);
                }
                else{
                    resolve(result);
                }
            });
        });
    }
}
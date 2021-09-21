const db = require('../config/db');
const mybatisMapper = require('mybatis-mapper');
mybatisMapper.createMapper(['./mapper/room.xml']);

module.exports = {

    getRoom : function(room_number){
        const query = mybatisMapper.getStatement('room', 'searchRoomByEmployeeNumber', data);
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
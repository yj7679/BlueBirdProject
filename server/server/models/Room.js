const db = require('../config/db');
const mybatisMapper = require('mybatis-mapper');
mybatisMapper.createMapper(['./mapper/room.xml']);

module.exports = {

    getRoom : function(name){
        console.log("search Room By: ", name)
        const query = mybatisMapper.getStatement('room', 'searchRoomByRoomName', name);
        return new Promise((resolve, reject)=>{
            db.query(query, (err, result, fields)=>{
                if(err){
                    console.log(err);
                    reject(err);
                }
                else{
                    // rawdatapacket to json
                    let ret = Object.values(JSON.parse(JSON.stringify(result)))

                    // no data : return null
                    if(Array.isArray(ret)&&ret.length===0){
                        ret = null;
                    }

                    resolve(ret);
                }
            });
        });
    }
}
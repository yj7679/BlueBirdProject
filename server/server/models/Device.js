const db = require('../config/db');
const mybatisMapper = require('mybatis-mapper');

mybatisMapper.createMapper(['./mapper/device.xml']);

module.exports = {
    getDevices : function(data){
        const query = mybatisMapper.getStatement('device', 'searchDevicesByRoomNumber', data);
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
    },
    searchDevice : function(data){
        const query = mybatisMapper.getStatement('device', 'searchDevice', data);
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
    },
    offDevice : function(data){
        const query = mybatisMapper.getStatement('device','offDeviceByPK', data);

        return new Promise((resolve, reject)=>{
            db.query(query, (err, result, fields)=>{
                if(err){
                    console.log(err);
                    reject(err);
                }
                else{
                    resolve(result);
                }
            })
        })
    }

}
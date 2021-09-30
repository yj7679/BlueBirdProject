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
    onDevice : function(data){
        const query = mybatisMapper.getStatement('device', 'onDeviceByPK', data);
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
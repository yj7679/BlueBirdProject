const db = require('../config/db');
const mybatisMapper = require('mybatis-mapper');

mybatisMapper.createMapper(['./mapper/employee.xml']);

module.exports = {

    getEmployee : function(data){
        const query = mybatisMapper.getStatement('employee', 'searchEmployeeByPK', data);
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
    insertEmployee : function(data){
        const query = mybatisMapper.getStatement('employee', 'insertEmployee', data);
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
    loginEmployee : function(data){
        const query = mybatisMapper.getStatement('employee', 'loginEmployee', data);
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
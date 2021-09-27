const express = require('express');
const Employee = require('../models/Employee');
const AuthController = require('./AuthController');

module.exports = {
    doGetEmployee : function(req, res, next){
        const employee_number = req.params.employeeNumber;
        const data = {
            'employee_number' : employee_number
        }

        console.log('search emplyee by number : ', employee_number);
        Employee.getEmployee(data).then((result)=>{
            res.send(result);
        })
    },
    doLoginEmployee : function(req, res, next){
        const data = {
            'id': req.body.id,
            'password': req.body.password,
        }

        console.log('login employee');
        Employee.loginEmployee(data).then((result)=>{
            const resultArray = Object.values(JSON.parse(JSON.stringify(result)));
            
            // 로그인 일치 정보 없음
            if(resultArray.length===0){
                res.send('login fail');
            }
            // 로그인 일치 정보 발견
            else{
                const eNum = resultArray[0].employee_number;
                const accessToken = AuthController.getAccessToken(eNum);
                res.cookie('accessToken', accessToken);
                res.send('login success');
            }
        })
    },
    doRegistEmployee : function(req, res, next){
        const data = {
            'room_number' : req.body.room_number,
            'id' : req.body.id,
            'name' : req.body.name,
            'password' : req.body.password,
            'company' : req.body.company,
            'department' : req.body.department,
            'job' : req.body.job,
            'x' : req.body.x,
            'y' : req.body.y,
        }
        
        console.log('insert employee');
        Employee.insertEmployee(data).then((result)=>{
            res.send(result);
        })
    }
}
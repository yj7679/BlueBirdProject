const express = require('express');
const Employee = require('../models/Employee');

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
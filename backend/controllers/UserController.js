const express = require('express');
const Users = require('../models/Users');
const Views = '../views/';

module.exports = {
    doGetUser : function(req, res, next){
        // req에서 id를 뽑아내는 작업.
        Users.getuser(id).then((result)=>{
            // res.render(Views+'index.ejs',{users:result});
            res.send(result);
        })
    }
}
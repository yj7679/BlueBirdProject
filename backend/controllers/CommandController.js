const express = require('express');
// const Command;

module.exports = {
    doVoiceDerive : function(req, res, next){
        const voiceCommand = req.body.command;

        // voiceCommand 에서 필요한 명령을 도출하는 작업
        // ...

        // 명령을 도출한 후 실행하는 작업
        // ...
    }
}
const express = require('express');
const router = express.Router();
const CommandController = require('../controllers/CommandController');

router.use(express.json())
router.use(express.urlencoded({extended:false}));

router.post('/voice', CommandController.doVoiceDerive);

module.exports = router;
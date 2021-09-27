const express = require('express');
const router = express.Router();
const DeviceController = require('../controllers/DeviceController');

router.use(express.json());
router.use(express.urlencoded({extended:false}));

// 방 내에 전자기기 조회
router.get('/:roomNumber', DeviceController.doGetDevices);

// 전자기기 on
router.post('/on', DeviceController.OnDevice);

// 전자기기 off
router.post('/off', DeviceController.OffDevice);


module.exports = router;
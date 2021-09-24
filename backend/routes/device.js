const express = require('express');
const router = express.Router();
const DeviceController = require('../controllers/DeviceController');

router.use(express.json());
router.use(express.urlencoded({extended:false}));

router.get('/:roomNumber', DeviceController.doGetDevices);
router.post('/deviceon', DeviceController.OnDevice);
router.post('/deviceoff', DeviceController.OffDevice);


module.exports = router;
const express = require('express');
const router = express.Router();
const EmployeeController = require('../controllers/EmployeeController');

router.use(express.json());
router.use(express.urlencoded({extended:false}));

router.get('/:employeeNumber', EmployeeController.doGetEmployee);
router.post('/join', EmployeeController.doRegistEmployee);

module.exports = router;
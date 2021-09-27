const express = require('express');
const router = express.Router();
const EmployeeController = require('../controllers/EmployeeController');

router.use(express.json());
router.use(express.urlencoded({extended:false}));

//employee 회원 정보 조회
router.get('/:employeeNumber', EmployeeController.doGetEmployee);

//로그인
router.post('/login', EmployeeController.doLoginEmployee);

//회원가입
router.post('/join', EmployeeController.doRegistEmployee);

module.exports = router;
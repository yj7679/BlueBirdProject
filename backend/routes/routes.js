const express = require('express');
const router = express.Router();
const userController = require('../controllers/UserController');


router.get('/users', userController.doGetUser);
router.post('/users/regist', userController.doRegistUser);

module.exports = router;
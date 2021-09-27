const dotenv = require('dotenv');
const jwt = require('jsonwebtoken');

dotenv.config();

module.exports = {
    getAccessToken : function(employeeNumber){
        const payload = {
            employee_number : employeeNumber
        }
        const secretkey = process.env.JWT_SECRETKEY;
        const option = {
            algorithm : process.env.JWT_ALGORITHM,
            expiresIn : process.env.JWT_EXPIRESIN,
            issuer : process.env.JWT_ISSUER
        }
        const token = jwt.sign(payload, secretkey, option);

        return token;
    }
}
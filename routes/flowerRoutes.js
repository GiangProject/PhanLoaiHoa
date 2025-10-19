const express = require('express');
const multer = require('multer');
const path = require('path');
const flowerController = require('../controllers/flowerController');

const router = express.Router();

// Cấu hình Multer để lưu file vào thư mục public/uploads
const storage = multer.diskStorage({
    destination: './public/uploads/',
    filename: function (req, file, cb) {
        cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
    }
});
const upload = multer({ storage: storage });


router.get('/', flowerController.getHomePage);
router.post('/upload', upload.single('flowerImage'), flowerController.classifyFlower);

module.exports = router;
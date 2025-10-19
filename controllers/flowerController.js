const path = require('path');
const { runPrediction } = require('../models/predictionModel');

// Hiển thị trang chủ
const getHomePage = (req, res) => {
    res.render('index', { predictions: null, imageFile: null });
};

// Xử lý upload và phân loại hoa
const classifyFlower = async (req, res) => {
    if (!req.file) {
        return res.status(400).render('index', {
            error: 'Vui lòng chọn một file ảnh.',
            predictions: null,
            imageFile: null
        });
    }

    const imagePath = req.file.path;
    const originalFilename = req.file.originalname;

    try {
        const result = await runPrediction(imagePath);

        // Tạo đường dẫn tương đối để hiển thị ảnh trên web
        const imageFileForView = path.join('uploads', req.file.filename);

        res.render('index', {
            predictions: result.predictions,
            imageFile: imageFileForView
        });

    } catch (error) {
        console.error(error);
        res.status(500).render('index', {
            error: 'Đã có lỗi xảy ra, vui lòng thử lại.',
            predictions: null,
            imageFile: null
        });
    }
};

module.exports = {
    getHomePage,
    classifyFlower,
};
// models/predictionModel.js

const { spawn } = require('child_process');
const path = require('path');

// Tự động xác định tên lệnh python (python, python3)
// và đường dẫn tới kịch bản
const pythonExecutable = process.platform === 'win32' ? 'python' : 'python3';
const pythonScriptPath = path.join(__dirname, '..', 'python_service', 'predict.py');

/**
 * Gọi kịch bản Python để dự đoán.
 * @param {string} imagePath Đường dẫn tới ảnh.
 * @returns {Promise<object>}
 */
function runPrediction(imagePath) {
    return new Promise((resolve, reject) => {
        // Gọi lệnh python chung, thay vì một đường dẫn cụ thể
        const pythonProcess = spawn(pythonExecutable, [pythonScriptPath, imagePath]);

        let resultData = '';
        pythonProcess.stdout.on('data', (data) => {
            resultData += data.toString();
        });

        let errorData = '';
        pythonProcess.stderr.on('data', (data) => {
            errorData += data.toString();
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                console.error(`Python Script Error: ${errorData}`);
                return reject(new Error('Lỗi xảy ra trong quá trình dự đoán. Kiểm tra lại môi trường Python và các thư viện.'));
            }
            try {
                const result = JSON.parse(resultData);
                resolve(result);
            } catch (e) {
                reject(new Error('Không thể phân tích kết quả từ Python.'));
            }
        });
    });
}

module.exports = { runPrediction };
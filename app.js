const express = require('express');
const path = require('path');
const flowerRoutes = require('./routes/flowerRoutes');

const app = express();
const port = 3000;

// Thiết lập View Engine là EJS
app.set('view engine', 'ejs');

// Phục vụ các file tĩnh từ thư mục public (CSS, JS, ảnh uploads)
app.use(express.static(path.join(__dirname, 'public')));

// Sử dụng router
app.use('/', flowerRoutes);

app.listen(port, () => {
    console.log(`Ứng dụng phân loại hoa đang chạy tại http://localhost:${port}`);
});
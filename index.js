const express = require('express');
const multer = require("multer");
const cors = require("cors");

const app = express();
app.use(cors());

const PORT ='5000' || process.env.PORT;

app.post('/upload',(req,res) =>{
    res.json({ file: 'uploaded file'});
});

app.listen(PORT ,() => console.log(`server listening on port ${PORT}`));
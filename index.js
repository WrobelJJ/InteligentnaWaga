const express = require('express');
const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.json());

app.post('/api/weights', (req, res) => {
    const weight = req.body.weight;
    console.log(`Otrzymano wagę: ${weight} kg`);
    res.status(200).send("Dane zapisane!");
});

app.listen(5000, () => {
    console.log('API działa na http://localhost:5000');
});

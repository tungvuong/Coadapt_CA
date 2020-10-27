 // server.js
import express from 'express';
import CA from './src/usingCA/controllers/juji';

const app = express()

app.use(express.json())

app.get('/', (req, res) => {
  return res.status(200).send({'message': 'YAY! Congratulations! Your first endpoint is working'});
});

app.post('/juji',CA.talk);

app.listen(443)
console.log('app running on port ', 443);

var spawn = require('child_process').spawn;

const CA = {
  /**
   * Create A CA
   * @param {object} req 
   * @param {object} res
   * @returns {object}
   */
  async talk(req, res) {
    if (!req.body.code || !req.body.content || !req.body.participantID || !req.body.responseTime) {
      return res.status(400).send({'message': 'Some values are missing'});
    }

    try {
      var process = spawn('python', ['./topicmodel/app.py']);
      process.stdout.on('data', function (data) {
            data = data.toString('utf8');
            return res.status(201).send({ "code": "questionCode", "topics": data });
        });

      return res.status(201).send({ "code": "questionCode", "topics": ["sleep","diet"] });
    } catch(error) {
      return res.status(400).send(error);
    }
  }
}

export default CA; 

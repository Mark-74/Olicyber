const express = require('express')
require('express-async-errors')
const { MongoClient } = require('mongodb')

const app = express()

app.use(express.static(__dirname + '/public'));

const PORT = 3000

let db = undefined;

(async () => {
    const client = new MongoClient('mongodb://root:REDACTED@db:27017');
    await client.connect()
    db = client.db('db')
    console.log('Connected to db')
})()


app.set('view engine', 'ejs');
app.use(express.json())

app.get('/', async (req, res) => {
    res.render('home.ejs')
})


app.get('/year', async (req, res) => {
    const year = parseInt(req.query.filter)
    let data = []

    if (year) {
        if (year === 1337) {
            data = [{
                'ಠ_ಠ': 'I segreti del gabibbo sono riservati'
            }]
        } else {
            data = await db.collection('info').find({ year }, { projection: { _id: 0 } }).toArray()
        }
    }

    res.render('year.ejs', { year, data })
})


app.get('/type', async (req, res) => {
    const type = req.query.filter
    let data = []

    if (type) {
        if (/secret/i.test(type)) {
            data = [{
                'ಠ_ಠ': 'I segreti del gabibbo sono riservati'
            }]
        } else {
            data = await db.collection('info').find({ type }, { projection: { _id: 0 } }).toArray()
        }
    }

    res.render('type.ejs', { type, data })
})


app.listen(PORT, () => {
    console.log(`Example app listening on port ${PORT}`)
})


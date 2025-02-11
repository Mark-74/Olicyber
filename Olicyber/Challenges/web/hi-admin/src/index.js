const express = require('express')
const merge = require('merge-objects')
const jwt = require('jsonwebtoken')
const { v4: uuidv4 } = require('uuid')
require('express-async-errors')

const app = express()
const PORT = 3000

const ADMIN_TOKEN = uuidv4() // randomized

app.set('view engine', 'ejs');

app.use(express.json())

// check auth
app.use(function (req, res, next) {
    if (req.query.token && req.query.token === ADMIN_TOKEN)
        res.locals.adminLogged = true
    next()
})

app.get('/', async (req, res) => {
    res.render('index')
})

app.get('/hi', async (req, res) => {
    res.render('present_form')
})

app.post('/hi', async (req, res) => {
    // default values
    let user = {
        name: 'random visitor',
        hobby: 'sleeping',
        age: '18',
    }

    merge(user, req.body)
    console.log(user)

    res.render('present_result', { user })
})


app.listen(PORT, () => {
    console.log(`Example app listening on port ${PORT}`)
})


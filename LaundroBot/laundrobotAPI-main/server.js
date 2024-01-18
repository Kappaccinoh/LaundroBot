const express = require('express')
const app = express()
const mongoose = require('mongoose');
const Washer = require('./items/washerModel')
const Dryer = require('./items/dryerModel')
const cors = require('cors');
const SeventeenDryer = require('./items/seventeenDryerModel');
const SeventeenWasher = require('./items/seventeenWasherModel');
app.use(cors())

app.use(express.json())

mongoose.connect('')
.then(() => {
    app.listen(3002, () => {
        console.log(`Node API app is running on port 3002`)
    })
    console.log('Connected to mongodb')
    
}).catch((e) => console.log(e))

//Routes

//ping
app.get('/', (req, res) => {
    res.send('hello Laundrobot Api')
})

//Add a washer
app.post('/addWasher', async(req, res) => {
    try {
        const washer = await Washer.create(req.body)
        res.status(200).json(washer);
    } catch (error) {
        console.log(error.message)
        res.status(500).json({message:error.message})
    }
})

//Add a nineteen washer
app.post('/addSeventeenWasher', async(req, res) => {
    try {
        const washer = await SeventeenWasher.create(req.body)
        res.status(200).json(washer);
    } catch (error) {
        console.log(error.message)
        res.status(500).json({message:error.message})
    }
})

//Add a dryer 
app.post('/addDryer', async(req, res) => {
    try {
        const dryer = await Dryer.create(req.body)
        res.status(200).json(dryer);
    } catch (error) {
        console.log(error.message)
        res.status(500).json({message:error.message})
    }
})

//Add a nineteen dryer 
app.post('/addSeventeenDryer', async(req, res) => {
    try {
        const dryer = await SeventeenDryer.create(req.body)
        res.status(200).json(dryer);
    } catch (error) {
        console.log(error.message)
        res.status(500).json({message:error.message})
    }
})

//get all washers
app.get('/washers', async(req, res) => {
    try {
        const washers = await Washer.find({}); // get all products
        //console.log('hi')
        res.status(200).json(washers)
    } catch (error) {
        //console.log('oh')
        res.status(500).json({message:error.message})
    }
})

//get all nineteen washers
app.get('/seventeenWashers', async(req, res) => {
    try {
        const washers = await SeventeenWasher.find({}); // get all products
        //console.log('hi')
        res.status(200).json(washers)
    } catch (error) {
        //console.log('oh')
        res.status(500).json({message:error.message})
    }
})

//get all nineteen dryers
app.get('/seventeenDryers', async(req, res) => {
    try {
        const dryers = await SeventeenDryer.find({}); // get all products
        res.status(200).json(dryers)
    } catch (error) {
        res.status(500).json({message:error.message})
    }
})

//get all dryers
app.get('/dryers', async(req, res) => {
    try {
        const dryers = await Dryer.find({}); // get all products
        res.status(200).json(dryers)
    } catch (error) {
        res.status(500).json({message:error.message})
    }
})


//update a washer
app.put('/washers/update', async(req, res) => {
    try{
        const washer_arr = await Washer.find({ "name": req.body["name"]});
        if (!washer_arr){
            return res.status(404).json({message: `cannot find any washers with this body ${req.body}`})
        }
        //console.log(req.body)
        let req_body_copy = req.body;
        let new_washer = washer_arr[0]
        //.log(req.body)
        new_washer['timeLeftUserInput'] = req.body['timeLeftUserInput']
        new_washer['endTime'] = req.body['endTime']
        //console.log(new_washer)
        //console.log('updated')
        const updatedwasher = await Washer.findByIdAndUpdate(new_washer['_id'], new_washer);
        res.status(200).json(updatedwasher);

    } catch (error) {
        res.status(500).json({message:error.message})
    }
})

//update a nineteen washer
app.put('/seventeenWashers/update', async(req, res) => {
    try{
        const washer_arr = await SeventeenWasher.find({ "name": req.body["name"]});
        if (!washer_arr){
            return res.status(404).json({message: `cannot find any washers with this body ${req.body}`})
        }
        //console.log(req.body)
        let req_body_copy = req.body;
        let new_washer = washer_arr[0]
        //.log(req.body)
        new_washer['timeLeftUserInput'] = req.body['timeLeftUserInput']
        console.log(req.body['endTime'])
        new_washer['endTime'] = req.body['endTime']
        //console.log(new_washer)
        console.log('updated')
        const updatedwasher = await SeventeenWasher.findByIdAndUpdate(new_washer['_id'], new_washer);
        res.status(200).json(updatedwasher);

    } catch (error) {
        res.status(500).json({message:error.message})
    }
})

//update a dryer
app.put('/dryers/update', async(req, res) => {
    try{
        const dryer_arr = await Dryer.find({ "name": req.body["name"]});
        if (!dryer_arr){
            return res.status(404).json({message: `cannot find any washers with this body ${req.body}`})
        }
        //console.log(req.body)
        let req_body_copy = req.body;
        let new_dryer = dryer_arr[0]
        
        new_dryer['timeLeftUserInput'] = req.body['timeLeftUserInput']
        new_dryer['endTime'] = req.body['endTime']
        //console.log(new_dryer)
        const updateddryer = await Dryer.findByIdAndUpdate(new_dryer['_id'], new_dryer);
        res.status(200).json(updateddryer);

    } catch (error) {
        res.status(500).json({message:error.message})
    }
})


//update a nineteen dryer
app.put('/seventeenDryers/update', async(req, res) => {
    try{
        const dryer_arr = await SeventeenDryer.find({ "name": req.body["name"]});
        if (!dryer_arr){
            return res.status(404).json({message: `cannot find any washers with this body ${req.body}`})
        }
        //console.log(req.body)
        let req_body_copy = req.body;
        let new_dryer = dryer_arr[0]
        
        new_dryer['timeLeftUserInput'] = req.body['timeLeftUserInput']
        new_dryer['endTime'] = req.body['endTime']
        //console.log(new_dryer)
        const updateddryer = await SeventeenDryer.findByIdAndUpdate(new_dryer['_id'], new_dryer);
        res.status(200).json(updateddryer);

    } catch (error) {
        res.status(500).json({message:error.message})
    }
})
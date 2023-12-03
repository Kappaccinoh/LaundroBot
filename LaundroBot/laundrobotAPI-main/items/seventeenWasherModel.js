const mongoose = require('mongoose')

const seventeenWasherSchema = mongoose.Schema(
    {
        name: {
            type:String,
            required: [true, "Please enter a washer name"]
        },
        timeLeftUserInput: {
            type: Number,
            required: true,
            default: 0
        },
        endTime: {
            type: String,
            required: false,
        },
    },
    {
        timestamps: true
    }
)

const SeventeenWasher = mongoose.model('SeventeenWasher', seventeenWasherSchema);

module.exports = SeventeenWasher;
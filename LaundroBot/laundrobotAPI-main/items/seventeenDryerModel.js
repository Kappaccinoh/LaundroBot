const mongoose = require('mongoose')

const seventeenDryerSchema = mongoose.Schema(
    {
        name: {
            type:String,
            required: [true, "Please enter a dryer name"]
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

const SeventeenDryer = mongoose.model('SeventeenDryer', seventeenDryerSchema);

module.exports = SeventeenDryer;
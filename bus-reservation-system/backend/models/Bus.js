const mongoose = require('mongoose');

const BusSchema = new mongoose.Schema({
    name: { type: String, required: true },
    seats: { type: Number, required: true },
    bookedSeats: { type: [Number], default: [] },
    date: { type: Date, required: true },
    source: { type: String, required: true },
    destination: { type: String, required: true },
});

const Bus = mongoose.model('Bus', BusSchema);
module.exports = Bus;

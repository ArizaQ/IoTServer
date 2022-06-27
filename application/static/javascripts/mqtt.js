
const MqttClient = require('./lib/client')
const connect = require('./lib/connect')
const Store = require('./lib/store')
const DefaultMessageIdProvider = require('./lib/default-message-id-provider')
const UniqueMessageIdProvider = require('./lib/unique-message-id-provider')

module.exports.connect = connect

// Expose MqttClient
module.exports.MqttClient = MqttClient
module.exports.Client = MqttClient
module.exports.Store = Store
module.exports.DefaultMessageIdProvider = DefaultMessageIdProvider
module.exports.UniqueMessageIdProvider = UniqueMessageIdProvider

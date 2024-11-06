const path = require('path');

module.exports = {
  entry: './index-sw.js',
  // The location of the build folder described above
  output: {
    path: path.resolve(__dirname, '../../static'),
    filename: './firebase-messaging-sw.js',
  },
  mode: 'production'
};
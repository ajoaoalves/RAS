var mongoose = require('mongoose');
const AWS = require('aws-sdk');
const { v4: uuidv4 } = require('uuid');

// Configure AWS SDK
const s3 = new AWS.S3({
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    region: process.env.AWS_REGION
});


var parametersSchema = new mongoose.Schema({
    // Specific Parameters for 'border'
    bordersize: { type: Number, required: false },
    bordercolor: { type: String, required: false },

    // Specific Parameters for 'brightness'
    brightnessValue: { type: Number, required: false },

    // Specific Parameters for 'crop'
    crop_box: {
        type: [Number], // Expecting an array of 4 numbers
        validate: {
            validator: function (v) {
                return !v || v.length === 4; // Validate if null/undefined or has exactly 4 elements
            },
            message: props => `O campo crop_box deve conter exatamente 4 números. Recebido: ${props.value.length}`,
        },
        required: false,
    },

    // Specific Parameters for 'resize'
    width: { type: Number, required: false },
    height: { type: Number, required: false },

    // Specific Parameters for 'rotation' and 'watermark'
    angle: { type: Number, required: false },

}, { _id: false });


var toolSchema = new mongoose.Schema({
    _id: String, 
    procedure: String,
    parameters: { type: [parametersSchema], required: false }
}, { _id: false });

var imageSchema = new mongoose.Schema({
    _id: String,
    uri: String 
}, { _id: false }); // Desativa o _id automático dos subdocumentos

var projectSchema = new mongoose.Schema({
    _id: String,
    name: String, 
    user_id: String,
    images: [imageSchema],
    tools: [toolSchema]
}, { versionKey: false });

module.exports = mongoose.model('projects', projectSchema);



// Upload image to S3 before saving
projectSchema.methods.uploadImageToS3 = async function (fileBuffer, fileName) {
    const bucketName = process.env.AWS_S3_BUCKET_NAME;
    const key = `images/${uuidv4()}-${fileName}`;

    try {
        const uploadResult = await s3.upload({
            Bucket: bucketName,
            Key: key,
            Body: fileBuffer,
            ContentType: 'image/jpeg', // Adjust for your image type
            ACL: 'public-read'
        }).promise();

        // Return the public URL of the uploaded image
        return uploadResult.Location;
    } catch (error) {
        throw new Error(`Failed to upload image to S3: ${error.message}`);
    }
};

// Add images to a project
projectSchema.methods.addImage = async function (fileBuffer, fileName) {
    const imageUrl = await this.uploadImageToS3(fileBuffer, fileName);

    this.images.push({ uri: imageUrl });
    await this.save();
};

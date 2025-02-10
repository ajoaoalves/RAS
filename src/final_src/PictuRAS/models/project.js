var mongoose = require('mongoose');
const AWS = require('aws-sdk');
const { v4: uuidv4 } = require('uuid');

// Configure AWS SDK
const s3 = new AWS.S3({
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    region: process.env.AWS_REGIO,
    endpoint: 'http://minio:9000', // MinIO endpoint URL
    s3ForcePathStyle: true // Required for MinIO
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
    _id: { type: String, default: uuidv4 },
    procedure: String,
    parameters: { type: parametersSchema, required: false }
}, { _id: false });

var imageSchema = new mongoose.Schema({
    _id: { type: String, default: uuidv4 },
    uri: String
}, { _id: false }); // Desativa o _id automático dos subdocumentos

var projectSchema = new mongoose.Schema({
    _id: { type: String, default: uuidv4 },
    name: String,
    user_id: String,
    images: [imageSchema],
    tools: [toolSchema]
}, { versionKey: false });


// Download an image from S3
projectSchema.methods.downloadImageFromS3 = async function (key) {
    const bucketName = process.env.AWS_S3_BUCKET_NAME;

    try {
        const params = {
            Bucket: bucketName,
            Key: key, // The S3 object key for the image
        };

        const image = await s3.getObject(params).promise();

        // Return the binary data and content type
        return {
            data: image.Body,
            contentType: image.ContentType,
        };
    } catch (error) {
        throw new Error(`Failed to download image from S3: ${error.message}`);
    }
};

// Upload image to S3 before saving
projectSchema.methods.uploadImageToS3FromBrowser = async function (fileBuffer, projectId) {
    const bucketName = process.env.AWS_S3_BUCKET_NAME;
    const key = `src/${projectId}/${uuidv4()}.jpg`;

    try {
        const uploadResult = await s3.upload({
            Bucket: bucketName,
            Key: key,
            Body: fileBuffer,
            ContentType: 'image/jpeg', // Adjust for your image type
            ACL: 'public-read'
        }).promise();

        // Return the public URL of the uploaded image
        return key;
    } catch (error) {
        throw new Error(`Failed to upload image to S3: ${error.message}`);
    }
};

// Add images to a project
projectSchema.methods.addImageFromBrowser = async function (fileBuffer, projectId) {
    const imageUrl = await this.uploadImageToS3FromBrowser(fileBuffer, projectId);

    this.images.push({ uri: imageUrl });
    await this.save();
};

projectSchema.methods.getImages = async function () {
    const bucketName = process.env.AWS_S3_BUCKET_NAME;

    try {
        // Map through stored image keys and download their data from S3
        const images = await Promise.all(
            this.images.map(async (image) => {
                const params = {
                    Bucket: bucketName,
                    Key: image.uri, // The S3 key stored in `images`
                };

                const s3Object = await s3.getObject(params).promise();

                return {
                    contentType: s3Object.ContentType, // Content type (e.g., image/png, image/jpeg)
                    data: s3Object.Body, // Binary image data
                };
            })
        );

        return images; // Return an array of image objects
    } catch (error) {
        throw new Error(`Failed to retrieve images from S3: ${error.message}`);
    }
};

module.exports = mongoose.model('projects', projectSchema);

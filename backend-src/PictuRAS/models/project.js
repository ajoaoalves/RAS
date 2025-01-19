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
    name: String,
    value: { type: mongoose.Schema.Types.Mixed }
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




// Upload image to S3 before saving
projectSchema.methods.uploadImageToS3FromBrowser = async function (fileBuffer, projectId) {
    const bucketName = process.env.AWS_S3_BUCKET_NAME;
    const key = `src/${projectId}/${uuidv4()}`;

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
projectSchema.methods.addImageFromBrowser = async function (fileBuffer, projectId) {
    const imageUrl = await this.uploadImageToS3FromBrowser(fileBuffer, projectId);

    this.images.push({ uri: imageUrl });
    await this.save();
};

module.exports = mongoose.model('projects', projectSchema);

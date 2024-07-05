import tensorflow as tf
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg19 import preprocess_input
from keras.applications.vgg19 import decode_predictions
from keras.applications.resnet50 import ResNet50

from flask import request, Flask, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES

model = ResNet50()
app = Flask(__name__)


def process_image(image):
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)
    return image


def predict_class(image):
    # predict the probability across all output classes
    yhat = model.predict(image)
    # convert the probabilities to class labels
    label = decode_predictions(yhat)
    # retrieve the most likely result, e.g. highest probability
    label = label[0][0]
    # return the classification
    prediction = label[1]
    percentage = '%.2f%%' % (label[2] * 100)
    return prediction, percentage


photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = './images'
configure_uploads(app, photos)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        # save the image
        img = request.files['photo']
        img_path = './images/' + img.filename
        img.save(img_path)
        # load the image
        image = load_img(img_path, target_size=(224, 224))
        # convert to numpy array
        image = img_to_array(image)
        # process the image
        proc_img = process_image(image)
        # make prediction
        prediction, percentage = predict_class(proc_img)
        # render the template with the prediction
        return render_template('home.html', prediction=prediction, percentage=percentage, image_path=img_path)
    # web page to show before the POST request containing the image
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

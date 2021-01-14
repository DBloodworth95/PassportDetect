import numpy as np
from tensorflow import keras


class Model:

    def predictEmotion(self, img):
        # Load the model
        loadedModel = keras.models.load_model("model/trained_model.h5")

        # Process image for normalizing.
        image = keras.preprocessing.image.load_img(img, grayscale=False, target_size=(150, 150))
        imageToPredict = keras.preprocessing.image.img_to_array(image)
        imageToPredict = np.expand_dims(imageToPredict, axis=0)
        imageToPredict /= 255

        # Store each potential class output in an array.
        # This array follows the same format that the output is produced by the model. (Alphabetically).
        emotionLabels = np.array([
            "angry",
            "fear",
            "happy",
            "neutral",
            "sad",
            "surprise"
        ])
        # Store the output prediction made by the Model (Stored as an array).
        predictionResult = loadedModel.predict(imageToPredict, verbose=1)
        # The numpy where() function is used in order to locate the highest value within the
        # entire array returned from the model. The index returned is then matched with
        # the index from the array storing each class as a String.
        # Once matched, the appropriate class is returned as a String.
        resultAsString = np.where(predictionResult[0] == np.amax(predictionResult[0]))

        # Debug - Prints the result of the prediction.
        print('Emotion Detected: ' + emotionLabels[resultAsString[0][0]])

        return emotionLabels[resultAsString[0][0]]

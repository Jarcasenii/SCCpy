from . import tools, pipeline

class Predictor:
    def predict(self, image_url):
        # pipeline will automatically load pretrained
        # weights for the detector and recognizer.
        pipe = pipeline.Pipeline()

        # Get a set of three example images
        images = [
            tools.read(image_url)
        ]

        # Each list of predictions in prediction is a list of
        # (word, box) tuples.
        prediction = pipe.recognize(images)[0]
        parsed_text = tools.parse(prediction)

        return parsed_text

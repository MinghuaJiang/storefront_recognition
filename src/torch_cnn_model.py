import lutorpy as lua
require("torch")
require("nn")
require("image")


imagenetClasses = torch.load('../model/alexnetowtbn_classes.t7')
meanStd = torch.load('../model/alexnetowtbn_meanStd.t7')
model = torch.load('../model/alexnetowtbn_epoch55_cpu.t7')
model._evaluate()


def preprocess(input_image):
    output_image = image.scale(input_image._clone(), 224, 224)

    for i in range(0, 3):
        output_image[i]._add(-meanStd.mean[i])
        output_image[i]._div(meanStd.std[i])
    return output_image


def predict(input_image):
    input_image = image.load(input_image, 3, 'float')
    input_image = image.scale(input_image, 224, 224)
    input_image = preprocess(input_image)._view(1, 3, 224, 224)
    predictions = model._forward(input_image)
    scores, class_ids = predictions[0]._exp()._sort(True)
    for i in range(0, 5):
        print('[%s] = %.5f' % (imagenetClasses[class_ids[i] - 1], scores[i]))

if __name__ == '__main__':
    predict('../model/bird.jpg')


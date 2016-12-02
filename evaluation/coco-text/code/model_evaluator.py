import coco_text
import coco_evaluation
class ModelEvaluator:
    def __init__(self):
        self.ct = coco_text.COCO_Text("../dataset/annotation/COCO_Text.json")
        print(self.ct.info())

    def evaluate(self, approach_name):
        our_results = self.ct.loadRes("../result/"+approach_name+".json")
        our_detections = coco_evaluation.getDetections(self.ct, our_results, detection_threshold=0.5)
        our_e2e_results = coco_evaluation.evaluateEndToEnd(self.ct, our_results, detection_threshold=0.5)
        coco_evaluation.printDetailedResults(self.ct, our_detections, our_e2e_results, approach_name)

if __name__ == '__main__':
    evaluator = ModelEvaluator()
    #evaluator.evaluate("a")
    #evaluator.evaluate("b")
    #evaluator.evaluate("c")
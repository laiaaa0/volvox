import unittest
import csv
import dome.track_volvox as tracker
import dome.dome_files.control_illum_main as ground_truth_script
from dome.detection import Detection

class TestMatching(unittest.TestCase):
    def __init__(self):
        with open('test/data/detections.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            self.__detected_list = {}
            header = next(reader)
            for row in reader:
                time_point = int(row[-1])
                detection = Detection(int(row[0]),int(row[1]), int(row[2]), int(row[3]), int(row[4]))
                if time_point in self.__detected_list:
                    self.__detected_list[time_point].append(detection)
                else:
                    self.__detected_list[time_point]= [detection]
        self.generate_ground_truth()

    def generate_ground_truth(self):        
        detected_list = {}
        with open('test/data/detections.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = next(reader)
            for row in reader:
                time_point = int(row[-1])
                detection = [int(row[0]),int(row[1]), int(row[2]),int(row[2]), int(row[3]), int(row[4])]
                if time_point in detected_list:
                    detected_list[time_point].append(detection)
                else:
                    detected_list[time_point]= [detection]
        matched_agents = []
        for i in range(1,50):
            matched_agents.append(ground_truth_script.agentMatching(detected_list[i],detected_list[i+1]))
        with open('test/ground_truth.csv', mode='w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect="excel")
            for i, row in enumerate(matched_agents):
                for detection in row:
                    l = list(detection[0:3])
                    l = l + list(detection[4:])
                    l.append(i)
                    writer.writerow(l)



        
    def test_matching(self):
        outputs = []
        for i in range(1,50):
            self.assertTrue(i in self.__detected_list and i+1 in self.__detected_list)
            outputs.append(tracker.match_detections(self.__detected_list[i],self.__detected_list[i+1]))

        with open('test/outputs.csv', mode='w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect="excel")
            for i,row in enumerate(outputs):
                for tracked in row:
                    l = tracked.to_list()
                    l.append(i)
                    writer.writerow(l)



if __name__=="__main__":
    s = TestMatching()
    s.test_matching()
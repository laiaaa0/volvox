import unittest
import filecmp
import csv
import dome.track_volvox as tracker
import dome.original_code.agent_matching as agent_matching_original
from dome.detection import Detection


def generate_ground_truth():
    detected_list = {}
    with open('test/data/detections.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        for row in reader:
            time_point = int(row[-1])
            detection = [
                int(row[0]), int(row[1]), # X Y
                int(row[2]), int(row[2]), # w h
                int(row[3]), int(row[4])] # deactivity
            if time_point in detected_list:
                detected_list[time_point].append(detection)
            else:
                detected_list[time_point] = [detection]
    matched_agents = []
    for i in range(1, 50):
        matched_agents.append(agent_matching_original.agentMatching(
            detected_list[i], detected_list[i + 1]))
    with open('test/ground_truth.csv', mode='w') as csvfile:
        writer = csv.writer(
            csvfile,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
            dialect="excel")
        for i, row in enumerate(matched_agents):
            for detection in row:
                l = list(detection[0:3])
                l = l + list(detection[4:])
                l.append(i)
                writer.writerow(l)


class TestMatching(unittest.TestCase):

    @classmethod
    def setUpClass(cls):    
        with open('test/data/detections.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            cls._detected_list = {}
            header = next(reader)
            for row in reader:
                time_point = int(row[-1])
                detection = Detection(int(row[0]), int(
                    row[1]), int(row[2]), int(row[3]), int(row[4]))
                if time_point in cls._detected_list:
                    cls._detected_list[time_point].append(detection)
                else:
                    cls._detected_list[time_point] = [detection]
        generate_ground_truth()


    def test_matching(self):
        outputs = []
        for i in range(1, 50):
            self.assertTrue(
                i in self._detected_list and 
                i + 1 in self._detected_list)
            next_detection =tracker.match_detections(
                self._detected_list[i], self._detected_list[i + 1]) 
            outputs.append(next_detection)
        
        with open('test/outputs.csv', mode='w') as csvfile:
            writer = csv.writer(
                csvfile,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                dialect="excel")
            for i, row in enumerate(outputs):
                for tracked in row:
                    l = tracked.to_list()
                    l.append(i)
                    writer.writerow(l)

        self.assertTrue(filecmp.cmp('test/outputs.csv', 'test/ground_truth.csv', shallow=False))

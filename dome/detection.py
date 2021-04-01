from simulation.geometry import Point
class Detection:
    def __init__(self, x,y,radius,a,b):
        self.__pos = Point(x,y)
        self.__r = radius


        # is either 0 or 1, with 0 meaning it is not detected in a given frame and 1 meaning that it is.
        self.__detected_in_current_frame = a 

        # the summation of this over subsequent frames, 
        # so if the agent is active and continues to be it will be incremented by 0.
        # If the agent is lost and becomes deactive, then this will become increasingly negative over time.
        self.__detections_last_frames = b 
    
    def position(self):
        return self.__pos
    
    def radius(self):
        return self.__r
    
    def to_list(self):
        return[self.__pos.x(),self.__pos.y(),self.__r,self.__detected_in_current_frame,self.__detections_last_frames]

    def update_deactivity(self):
        self.__detections_last_frames = self.__detections_last_frames + (self.__detected_in_current_frame -1)

    def reset_deactivity(self):
        self.__detected_in_current_frame = 0

    def is_active(self):
        return self.__detections_last_frames > -3

    def distance(self, other_detection):
        return self.position().distance(other_detection.position())

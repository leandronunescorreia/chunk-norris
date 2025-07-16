from abc import ABC, abstractmethod

class Detector(ABC):
    @abstractmethod
    def detect(self, input_data):
        """
        Perform detection on the given input data.

        Args:
            input_data: The data to be analyzed by the detector.

        Returns:
            The result of the detection process.
        """
        pass
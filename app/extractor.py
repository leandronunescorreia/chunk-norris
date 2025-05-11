from abc import ABC, abstractmethod

class Extractor(ABC):
    @abstractmethod
    def extract(self, input_data):
        """
        Perform detection on the given input data.

        Args:
            input_data: The data to be analyzed by the detector.

        Returns:
            The result of the detection process.
        """
        pass
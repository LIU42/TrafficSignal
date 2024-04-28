import numpy
import torch
import cv2
import math

from utils import PlottingUtils

class TrafficLight:

    def __init__(self, center_x: int, center_y: int, width: int, height: int, color: str, shape: str = None) -> None:
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.color = color
        self.shape = shape

    def __str__(self) -> str:
        return f"{self.center_x} {self.center_y} {self.width} {self.height} {self.color} {self.shape}"

    def __eq__(self, other: 'TrafficLight') -> bool:
        return self.rect_xywh == other.rect_xywh
    
    def __hash__(self) -> int:
        return hash(self.center_x) + hash(self.center_y) + hash(self.width) + hash(self.height)
    
    @property
    def rect_xywh(self) -> tuple[int, int, int, int]:
        return int(self.center_x), int(self.center_y), int(self.width), int(self.height)
    
    @property
    def rect_xyxy(self) -> tuple[int, int, int, int]:
        x1 = self.center_x - self.width // 2
        y1 = self.center_y - self.height // 2
        x2 = self.center_x + self.width // 2
        y2 = self.center_y + self.height // 2
        return int(x1), int(y1), int(x2), int(y2)
    
    def similarity_to(self, other: 'TrafficLight', weight_x: float = 0.05, weight_y: float = 5, weight_size: float = 2) -> float:
        distance_x = weight_x * (self.center_x - other.center_x)
        distance_y = weight_y * (self.center_y - other.center_y)
        distance_size = weight_size * (abs(self.width - other.width) + abs(self.height - other.height))
        return math.sqrt(distance_x ** 2 + distance_y ** 2) + distance_size
    
    @staticmethod
    def similarity(cluster1: set['TrafficLight'], cluster2: set['TrafficLight']) -> float:
        min_distance = math.inf
        for traffic_light1 in cluster1:
            for traffic_light2 in cluster2:
                min_distance = min(traffic_light1.similarity_to(traffic_light2), min_distance)
        return min_distance
    
    @staticmethod
    def center_distance(cluster: set['TrafficLight'], x: float = 320, y: float = 240) -> float:
        average_center_x = numpy.mean([ traffic_light.center_x for traffic_light in cluster ])
        average_center_y = numpy.mean([ traffic_light.center_y for traffic_light in cluster ])
        return math.sqrt((average_center_x - x) ** 2 + (average_center_y - y) ** 2)
    
    def set_radical(self) -> None:
        if self.color != "red":
            self.color = "green"

    def set_conservative(self) -> None:
        if self.color != "green":
            self.color = "red"
    
    def plot(self, image: cv2.Mat) -> cv2.Mat:
        return PlottingUtils.plot_traffic_light(image, *self.rect_xyxy, self.color, self.shape)


class TrafficLightBuilder:

    @staticmethod
    def from_xywh(xywh_tensor: torch.Tensor, color: str) -> TrafficLight:
        center_x, center_y, width, height = xywh_tensor
        return TrafficLight(int(center_x), int(center_y), int(width), int(height), color)


class TrafficSignal:

    def __init__(self, strategy: str = "conservative") -> None:
        assert strategy == "radical" or strategy == "conservative"
        if strategy == "radical":
            self.straight = True
            self.left = True
            self.right = True
        elif strategy == "conservative":
            self.straight = False
            self.left = False
            self.right = True
    
    def __str__(self) -> str:
        return f"Straight: {str(self.straight):<8}Left: {str(self.left):<8}Right: {str(self.right):<8}"
    
    def all_allow(self) -> None:
        self.straight = True
        self.left = True
        self.right = True

    def all_forbid(self) -> None:
        self.straight = False
        self.left = False
        self.right = True

    def plot(self, image: cv2.Mat) -> cv2.Mat:
        image = PlottingUtils.plot_signal(image, "Straight", 55, self.straight)
        image = PlottingUtils.plot_signal(image, "Left", 5, self.left)
        image = PlottingUtils.plot_signal(image, "Right", 145, self.right)
        return image
    
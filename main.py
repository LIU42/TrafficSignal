import cv2
import os
import timeit

from solution import TrafficSignalSolution

class Main:

    def __init__(self) -> None:
        self.solution = TrafficSignalSolution()

    def images_predict(self, image_path: str = "./images", result_path: str = "./results") -> None:
        total_times = 0
        image_count = 0
        for image_index, image_name in enumerate(os.listdir(image_path), start = 0):
            image = cv2.imread(f"{image_path}/{image_name}")
            start_times = timeit.default_timer()
            signal = self.solution(image, plot_result = True)
            delta_times = timeit.default_timer() - start_times
            if image_index > 0:
                total_times += delta_times
                image_count += 1
            cv2.imwrite(f"{result_path}/result_{image_name}", image)
            print(f"Image: {image_name:<10}{signal}Times: {delta_times:.3f}s")
        print(f"\nAverage Times: {total_times / image_count:.3f}s\n")

    def camera_predict(self, camera: int = 0, window_name: str = "Camera Predict") -> None:
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        capture = cv2.VideoCapture(camera)
        while cv2.waitKey(1) != ord("q"):
            start_times = timeit.default_timer()
            frame = capture.read()[1]
            self.solution(frame, plot_result = True)
            cv2.imshow(window_name, frame)
            print(f"\rFPS: {1 / (timeit.default_timer() - start_times):.2f}", end = "")      
        capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    Main().images_predict()

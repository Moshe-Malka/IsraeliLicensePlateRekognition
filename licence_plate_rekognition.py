import re, os
import boto3
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

reko_client = boto3.client('rekognition')
pat_pre = re.compile("[0-9]{3}.+[0-9]{2}.+[0-9]{3}")  # israeli license plate (after 2017)
pat_post = re.compile("[0-9]{2}.+[0-9]{3}.+[0-9]{2}")  # israeli license plate (before 2017)

def read_image_file(path):
    with open(path, 'rb') as image_file:
        return image_file.read()

def detect_text(image_bytes):
    response = reko_client.detect_text(Image={'Bytes': image_bytes})
    return response

def filter_matched_regex(detections):
    detected_text = [ x['DetectedText'] for x in  detections['TextDetections'] ]
    filtered = [ x for x in detected_text if len(re.findall(pat_pre, x))>0 or len(re.findall(pat_post, x))>0 ]
    # filtered = list(filter(lambda x: len(re.findall(pat_pre, x)) or len(re.findall(pat_post, x)), detected_text))
    return filtered

def process_one_image(fname):
    raw_image = read_image_file(fname)
    detections = detect_text(raw_image)
    matched = filter_matched_regex(detections)
    return matched

def main():
    # files = [x for x in os.listdir() if 'lp' in x and not os.path.isdir(x)] # change this to your files
    files = ["/Users/moshemalka/Desktop/lp6.jpg"]
    for filename in files:
        matched = process_one_image(filename)
        for match in matched:
            print(match)
            # Optional : show file with matched pattern
            # img = mpimg.imread(filename)
            # plt.imshow(img)
            # plt.axis('off')
            # plt.text(0.5, 0.5, match, fontsize=12)
            # plt.show()

if __name__ == '__main__':
    main()
    
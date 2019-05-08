import os
import json
import editdistance
import numpy as np
from keras.applications.resnet50 import ResNet50
from scipy.spatial.distance import cosine

model = ResNet50(weights="imagenet")
weights = model.layers[-1].get_weights()[0].transpose()
print weights.shape

flatten = lambda l: [item for sublist in l for item in sublist]

class_index_file_url = "https://raw.githubusercontent.com/Lasagne/Recipes/master/examples/resnet50/imagenet_classes.txt"

if os.path.isfile("imagenet_classes.txt"):
    print "Class index file downloaded"
else:
    print "Downloading class index"
    os.popen("wget " + class_index_file_url).read()

class_index = dict(list(zip(range(1000), open("imagenet_classes.txt").read().split("\n"))))

while True:
    print "Command: "
    command = raw_input().split(" ")
    if command[0] == "class":
        sci = int(command[1])
        print "Class: \"" + class_index[sci] + "\""
    elif command[0] == "similar":
        sci = int(command[1])
        print "Classes similar to \"" + class_index[sci] + "\":"
        looking_for_class = weights[sci]
        distances = np.array([cosine(looking_for_class, x) for x in weights])
        inv_dist = np.max(distances) - distances
        inv_dist = inv_dist.argsort()[-6:][::-1]
        inv_dist = inv_dist[1:]
        print "\n".join([str(x[0]) + ": " + class_index[x[1]] for x in zip(range(5), inv_dist)])


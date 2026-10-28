import tensorflow as tf
import sys
import os


# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf


def classify_image(filepath):
    # image_path = sys.argv[1]
    # image_path="C:\\Users\\ELCOT-Lenovo\\Documents\\images\\sign_dataset\\test\\A\\color_0_0016"
    # Read the image_data
    image_data = tf.gfile.FastGFile(filepath, 'rb').read()


    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                       in tf.gfile.GFile(r"C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\logs\output_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile(r"C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\logs\output_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
            return human_string, round(score*100, 2)


output_data={
    "apple black rot":{"plant":"Apple", "disease":"Black Rot"},
    "apple apple scab":{"plant":"Apple", "disease":"Apple Scab"},
    "apple cedar apple rust":{"plant":"Apple", "disease":"Cedar Apple Rust"},
    "tomato septoria leaf spot":{"plant":"Tomato", "disease":"Septoria Leaf Spot"},
    "tomato bacterial spot":{"plant":"Tomato", "disease":"Bacterial Spot"},
    "apple healthy":{"plant":"Apple", "disease":"Healthy"},
    "tomato healthy":{"plant":"tomato", "disease":"healthy"},
    "pepper bell bacterial spot":{"plant":"pepper", "disease":"bell bacterial spot"},
    "tomato early blight":{"plant":"tomato", "disease":"early blight"},
    "tomato target spot":{"plant":"tomato", "disease":"target spot"},
    "tomato tomato mosaic virus":{"plant":"tomato", "disease":"tomato mosaic virus"},
    "pepper bell healthy":{"plant":"pepper", "disease":"bell healthy"},
    "tomato tomato yellowleaf curl virus":{"plant":"tomato", "disease":"tomato yellowleaf curl virus"},
    "corn maize cercospora leaf spot gray leaf spot":{"plant":"corn", "disease":"maize cercospora leaf spot gray leaf spot"},
    "tomato leaf mold":{"plant":"tomato", "disease":"leaf mold"},
    "corn maize healthy":{"plant":"corn maize", "disease":"healthy"},
    "corn maize common rust":{"plant":"corn maize", "disease":"common rust"},
    "corn maize northern leaf blight":{"plant":"corn maize", "disease":"northern leaf blight"},
}

# data, score = classify_image(r"C:\Users\alen kurian\OneDrive\Pictures\Dataset\Potato___healthy\1ae826e2-5148-47bd-a44c-711ec9cc9c75___RS_HL 1954.jpg")
# print("Plant name  ", output_data[data]['plant'])
# print("Disease name  ", output_data[data]['disease'])
# print("Matching Score  ", score, "%")
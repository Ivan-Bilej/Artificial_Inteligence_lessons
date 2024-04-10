import tensorflow as tf
import numpy as np
import matplotlib as plt


def show_sample(s, c):

    plt.figure()
    plt.imshow(s, cmap=plt.cm.binary)
    plt.colorbar()
    plt.grid(False)
    plt.title(c)
    plt.show()


# zobrazí predikci vzorku číslo i
def sample_predict(i, test_images, test_labels, predictions, class_names):
    s = test_images[i]
    c = class_names[test_labels[i]]
    show_sample(s, c)

    print("Probabilities")
    print("------------")
    for j in range(len(class_names)):
        print(class_names[j], ":", np.round(predictions[i, j], 2))

    ind = np.argmax(predictions[i])

    print("------------")
    print("true class:", c, ", predicted class:", class_names[ind])


def main():
    (train_images, train_labels), (test_images, test_labels) = ai_dataset.load_data()
    train_images = train_images / 255.0  # normalizace dat - původní od 0 do 255
    test_images = test_images / 255.0

    class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    show_sample(train_images[0], class_names[train_labels[0]])

    for i in range(5):
        show_sample(train_images[i], class_names[train_labels[i]])

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),  # transformuje 2D obrazek do 1D vektoru
        tf.keras.layers.Dense(128, activation='sigmoid'),
        tf.keras.layers.Dense(10)
    ])
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=10)
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    pr_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()]) # přidání softmax vrstvy
    predictions = pr_model.predict(test_images)
    sample_predict(102, test_images, test_labels, predictions, class_names)


if __name__ == "__main__":
    ai_dataset = tf.keras.dataset.mnist

    main()
import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pathlib
import tensorflow_datasets as tfds


def show_sample(smp, cls):
    plt.figure()
    plt.imshow(smp)
    plt.colorbar()
    plt.grid(False)
    plt.title(cls)
    plt.show()


def show_training_sample_result(history, epochs):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()


def normalize(dataset_images):
    return dataset_images / 255.0


def process_image_samples(dataset, classes, amount=1):
    for images, labels in dataset.take(1):
        for i in range(amount):
            show_sample(images[i].numpy().astype("uint8"),
                        classes[labels[i]])
            """
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(classes[labels[i]])
            plt.axis("off")
            plt.colorbar()
            plt.grid(False)
            plt.show()
            """


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
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    """

    (train_ds, val_ds), ds_info = tfds.load(
        "cifar10",
        split=["train", "test"],
        batch_size=batch_size,
        as_supervised=True,
        with_info=True,
    )


    print(ds_info.features['label'].names)
    class_names = ds_info.features['label'].names
    print(class_names)
    """

    class_names = train_ds.class_names

    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    #for image_batch, labels_batch in train_ds:
    #    print(image_batch)
    #    print(labels_batch)
    #    break

    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal_and_vertical"),
        tf.keras.layers.RandomRotation(0.2),
        tf.keras.layers.RandomZoom(0.2),
        tf.keras.layers.RandomContrast(0.2),
        tf.keras.layers.RandomTranslation(0.1, 0.1)
    ])

    model = tf.keras.Sequential([
        tf.keras.layers.Rescaling(1. / 255),
        data_augmentation,
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(32, 3, padding="same", activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, padding="same", activation='relu'),
        #tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, padding="same", activation='relu'),
        #tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(len(class_names), name="outputs")
    ])

    #process_image_samples(train_ds, class_names, amount=1)

    model.compile(
        optimizer='adamax',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])

    model.summary()

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )

    model.summary()
    show_training_sample_result(history, epochs)

    pr_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])  # přidání softmax vrstvy
    predictions = pr_model.predict(train_ds)


if __name__ == "__main__":
    dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
    #"https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
    # Dataset for leaves: 4502 images, 22 categories
    # https://data.mendeley.com/datasets/hb74ynkjcn/1
    # Dataset for Calltech_101
    # "https://data.caltech.edu/records/mzrjq-6wc02/files/caltech-101.zip?download=1"

    archive = tf.keras.utils.get_file(origin=dataset_url, extract=True)
    data_dir = pathlib.Path(archive).with_suffix('')
    # print(data_dir)
    # print(pathlib.Path.cwd())

    batch_size = 16
    img_width = 128
    img_height = 128

    #image_count = len(list(data_dir.glob('*/*.jpg')))
    #print(image_count)

    AUTOTUNE = tf.data.AUTOTUNE
    epochs = 20

    main()
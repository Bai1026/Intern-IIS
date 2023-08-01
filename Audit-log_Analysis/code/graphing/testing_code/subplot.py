import os as os
import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

def plot_images_in_subplots():
    directory = "../graphs/graph_benign2/"  # the directory where you stored your images
    files = [f for f in os.listdir(directory) if f.endswith('.png')]  # get all .png files in the directory

    n = len(files)  # the number of images
    n_cols = 3  # number of columns in the subplot
    n_rows = n // n_cols + (n % n_cols > 0)  # calculate number of rows needed

    fig, ax = plt.subplots(n_rows, n_cols, figsize=(n_cols * 6, n_rows * 6))

    for i, file in enumerate(files):
        img = plt.imread(os.path.join(directory, file))  # read the image
        ax[i // n_cols, i % n_cols].imshow(img)  # plot image
        ax[i // n_cols, i % n_cols].axis('off')  # hide the axis
        label = file.split('_')[0] + '_' + file.split('_')[1][:3]
        ax[i // n_cols, i % n_cols].set_title(label)  # set the file name as title

    plt.tight_layout()
    plt.show()

plot_images_in_subplots()

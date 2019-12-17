import os
import random
from PIL import Image
import skimage as sk
from skimage import transform
from skimage import util
from skimage import io
import np

input_data = {
    "login": {
        "folder_path": 'input_data/login',
        "output_path": "augmented_data/login",
        "num_files_desired": 500
    },
    "dashboard": {
        "folder_path": 'input_data/dashboard',
        "output_path": "augmented_data/dashboard",
        "num_files_desired": 1000
    },
    "view": {
        "folder_path": 'input_data/view',
        "output_path": "augmented_data/view",
        "num_files_desired": 1000
    },
    "views": {
        "folder_path": 'input_data/views',
        "output_path": "augmented_data/views",
        "num_files_desired": 1000
    },
    "create_view": {
        "folder_path": 'input_data/create_view',
        "output_path": "augmented_data/create_view",
        "num_files_desired": 1000
    },
}


def random_rotation(image_array):
    # pick a random degree of rotation between 25% on the left and 25% on the right
    random_degree = random.uniform(-25, 25)
    return sk.transform.rotate(image_array, random_degree)


def random_noise(image_array):
    # add random noise to the image
    return sk.util.random_noise(image_array)


def horizontal_flip(image_array):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]


# dictionary of the transformations we defined earlier
available_transformations = {
    'rotate': random_rotation,
    'noise': random_noise,
    'horizontal_flip': horizontal_flip
}


def create_augmented_dataset(web_page):
    folder_path = input_data[web_page]["folder_path"]
    output_path = input_data[web_page]["output_path"]
    num_files_desired = input_data[web_page]["num_files_desired"]
    # find all files paths from the folder
    images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
              os.path.isfile(os.path.join(folder_path, f))]

    num_generated_files = 0
    while num_generated_files <= num_files_desired:
        print num_generated_files
        # random image from the folder
        image_path = random.choice(images)
        # read image as an two dimensional array of pixels
        image_to_transform = sk.io.imread(image_path)
        # random num of transformation to apply
        num_transformations_to_apply = random.randint(1, len(available_transformations))

        num_transformations = 0
        transformed_image = None
        while num_transformations <= num_transformations_to_apply:
            # random transformation to apply for a single image
            print "number of trasformations applied {}".format(num_transformations)
            key = random.choice(list(available_transformations))
            transformed_image = available_transformations[key](image_to_transform)
            num_transformations += 1

        new_file_path = '%s/augmented_image_%s.jpg' % (output_path, num_generated_files)
        im = Image.fromarray((transformed_image * 255).astype(np.uint8))
        rgb_im = im.convert('RGB')
        rgb_im.save(new_file_path)
        num_generated_files += 1


if __name__ == '__main__':
    #create_augmented_dataset("login")
    #create_augmented_dataset("dashboard")
    create_augmented_dataset("view")
    create_augmented_dataset("views")
    create_augmented_dataset("create_view")

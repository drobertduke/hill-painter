import numpy as np
from PIL import Image, ImageChops


def plt_circle(np_image, cx, cy, radius, color):
    top = max(-radius, -cy)
    bottom = min(radius, np_image.shape[0] - cy)
    left = max(-radius, -cx)
    right = min(radius, np_image.shape[1] - cx)
    # y, x = np.ogrid[-radius: radius, -radius: radius]
    y, x = np.ogrid[top: bottom, left: right]
    index = x**2 + y**2 <= radius**2
    y_start = max(cy-radius, 0)
    x_start = max(cx-radius, 0)
    y_end = min(cy+radius, np_image.shape[0])
    x_end = min(cx+radius, np_image.shape[1])
    np_image[y_start:y_end, x_start:x_end][index] = color
        # np_image[cy-radius:cy+radius, cx-radius:cx+radius][index] = color



def get_score(painting, model):
    diff = ImageChops.difference(model, painting)
    return int(np.array(diff).sum())


def invoke(args):
    model = Image.open(args.image_path)
    painting = Image.new('RGB', model.size)
    start_radius = 100
    radius = start_radius
    score = get_score(painting, model)
    attempts = 10
    for _ in range(args.iterations):
        new_painting, new_score = step(painting, model, radius)
        improvement = score - new_score
        if improvement <= 0:
            attempts -= 1
            if attempts <= 0:
                radius -= 1
                attempts = 10
        else:
            painting = new_painting
            score = new_score

        if radius <= 10:
            radius = start_radius
    print(score)
    print(radius)

    save_image(painting)


def step(painting, model, radius):
    new_painting = random_draw(painting, radius)
    new_score = get_score(new_painting, model)
    return new_painting, new_score


def random_draw(painting, radius):
    np_image = np.array(painting)
    cy = int(np.random.random_sample() * np_image.shape[0])
    cx = int(np.random.random_sample() * np_image.shape[1])
    color = [
        ((np.random.random_sample() * 255) + 255) / 2,
        ((np.random.random_sample() * 255) + 255) / 2,
        ((np.random.random_sample() * 255) + 255) / 2,
    ]
    plt_circle(np_image, cx, cy, radius, color)
    return Image.fromarray(np_image)


def save_image(image):
    image.save("tiger_result.png", "PNG")



import glob
import os

import numpy as np

data_path = 'UCF101_train'
NUM = 276918

classes = glob.glob(os.path.join(data_path, '**'))
print(len(classes))

# count suppose frame counts of each class
total_counts = 0
class_counts = []
for i in range(len(classes)):
    png_files = glob.glob(os.path.join(classes[i], '*.png'))
    print('class ' + str(i) + ': ' + str(len(png_files)))
    class_counts.append(len(png_files))
    total_counts += len(png_files)

filtered_counts = []
for i in range(len(classes)):
    filtered_counts.append(int(float(NUM)*class_counts[i]/float(total_counts)))
    print('filtered class ' + str(i) + ': ' + str(filtered_counts[i]))

def psnr(x1, x2):
    MSE = np.mean(np.square(x1-x2))
    MSE = np.maximum(MSE, 1e-10)
    return 10 * np.log10(1 / MSE)



"""for training set"""
# calculate PSNR and sort
f0 = open('frame1.txt', 'w')
f1 = open('frame2.txt', 'w')
f2 = open('frame3.txt', 'w')
for i in range(len(classes)):
    print('filtering... ' + str(i))
    triplets_dict = []
    png_files = glob.glob(os.path.join(classes[i], '*.png'))
    png_files = sorted(png_files)
    for j in range(1, len(png_files)-1):
        idx = int(png_files[j][-8:-4])
        if png_files[j-1] == (png_files[j][:-8] + str(idx-1).zfill(4) + '.png') \
            and png_files[j+1] == (png_files[j][:-8] + str(idx+1).zfill(4) + '.png'):
            triplets_dict.append(png_files[j])

    for j in range(filtered_counts[i]):
        idx = int(triplets_dict[j][-8:-4])
        f0.write('./'+triplets_dict[j][:-8] + str(idx-1).zfill(4) + '.png' + '\n')
        f1.write('./'+triplets_dict[j][:-8] + str(idx).zfill(4) + '.png' + '\n')
        f2.write('./'+triplets_dict[j][:-8] + str(idx+1).zfill(4) + '.png' + '\n')

f0.close()
f1.close()
f2.close()

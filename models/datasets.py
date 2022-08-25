import tensorflow as tf
from tensorflow import keras
from treelib import Tree
import numpy as np

from emnist import list_datasets, extract_training_samples, extract_test_samples


def DatasetTree(level_maps):
    """
    provide levels maps as a list of class level maps! Prioritising from coarse to fine levels.
    Works only for hierarchy with 2 and 3 levels.
    """
    levels = len(level_maps)
    
    tree = Tree()
    tree.create_node("Root", "root")  # root node

        
    tree = Tree()
    tree.create_node("Root", "root")  # root node
    
    if levels == 1:
        for i in range(len(set(level_maps[0].values()))):
            tree.create_node('Coarse_'+str(i), 'L0_'+ str(i), parent="root")
            for j in range(len(level_maps[0])):
                if level_maps[0][j] == i :
                    tree.create_node('Fine_'+str(j), 'L1_'+str(j), 'L0_'+ str(i))
                    
    elif levels == 2:
        for i in range(len(set(level_maps[0].values()))):
            tree.create_node('Coarse_'+str(i), 'L0_'+ str(i), parent="root")
            for j in range(len(level_maps[0])):
                if level_maps[0][j] == i :
                    tree.create_node('Medium'+str(j), 'L1_'+str(j), 'L0_'+ str(i))
                    for k in range(len(level_maps[1])):
                        if level_maps[1][k] == j :
                            tree.create_node('Fine_'+str(k), 'L2_'+str(k), 'L1_'+ str(j))
                
    return tree

def MNIST():
    """
    This is a Manually constructed hierarchical Dataset for MNIST dataset.
    It has 2 hierarchical levels (COARSE and FINE level)
    Coarse classes = 5; Fine Classes = 10.
    :return:
    :X_train:
    :Y_train:
    :X_test:
    :X_test:
    :tree: Digraph
    """
    MNIST = keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = MNIST.load_data()
    
    #--- coarse classes ---
    num_coarse = 5
    #--- fine classes ---
    num_fine  = 10
    #-------------------- data loading ----------------------
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    y_train_fine = keras.utils.to_categorical(y_train, num_fine)
    y_test_fine = keras.utils.to_categorical(y_test, num_fine)

    x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.
    x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.
    
    #---------------------- make coarse labels --------------------------
    fine_coarse = {0:0, 1:2, 2:1, 3:4, 4:3, 5:4, 6:0, 7:2, 8:1, 9:3}
    y_train_coarse = np.zeros((y_train_fine.shape[0], num_coarse)).astype("float32")
    y_test_coarse = np.zeros((y_test_fine.shape[0], num_coarse)).astype("float32")
    for i in range(y_train_coarse.shape[0]):
        y_train_coarse[i][fine_coarse[np.argmax(y_train_fine[i])]] = 1.0
    for i in range(y_test_coarse.shape[0]):
        y_test_coarse[i][fine_coarse[np.argmax(y_test_fine[i])]] = 1.0
        
    tree = DatasetTree([fine_coarse])
    
    
    return x_train, y_train_coarse, y_train_fine, x_test, y_test_coarse, y_test_fine, tree
    
def E_MNIST():
    from emnist import list_datasets, extract_training_samples, extract_test_samples
    print(list_datasets()) ## PRINT contents of the datasets

    x_train, y_train = extract_training_samples('balanced')
    print('Complete loading training samples as: x_train, y_train')
    x_test, y_test = extract_test_samples('balanced')
    print('Complete loading test samples as: x_test, y_test')

    #--- coarse classes ---
    num_coarse = 2
    #--- fine classes ---
    num_fine  = 47

    #-------------------- data loading ----------------------
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    y_train_fine = keras.utils.to_categorical(y_train, num_fine)
    y_test_fine = keras.utils.to_categorical(y_test, num_fine)

    # #---------------- data preprocessiong -------------------
    # x_train = (x_train-np.mean(x_train)) / np.std(x_train)
    # x_test = (x_test-np.mean(x_test)) / np.std(x_test)

    x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.
    x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.
    #---------------------- make coarse labels --------------------------
    fine_coarse = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:1,18:1,19:1,20:1,
                   21:1,22:1,23:1,24:1,25:1,26:1,27:1,28:1,29:1,30:1,31:1,32:1,33:1,34:1,35:1,36:1,37:1,38:1,39:1,
                   40:1,41:1,42:1,43:1,44:1,45:1,46:1}

    y_train_coarse = np.zeros((y_train_fine.shape[0], num_coarse)).astype("float32")
    y_test_coarse = np.zeros((y_test_fine.shape[0], num_coarse)).astype("float32")
    for i in range(y_train_coarse.shape[0]):
        y_train_coarse[i][fine_coarse[np.argmax(y_train_fine[i])]] = 1.0
    for i in range(y_test_coarse.shape[0]):
        y_test_coarse[i][fine_coarse[np.argmax(y_test_fine[i])]] = 1.0
        
    tree = DatasetTree([fine_coarse])
    
    return x_train, y_train_coarse, y_train_fine, x_test, y_test_coarse, y_test_fine, tree
    

def F_MNIST():
    F_MNIST = keras.datasets.fashion_mnist
    (x_train, y_train), (x_test, y_test) = F_MNIST.load_data()
    #--- coarse 1 classes ---
    num_coarse_1 = 2
    #--- coarse 2 classes ---
    num_coarse_2 = 6
    #--- fine classes ---
    num_fine  = 10
    #-------------------- data loading ----------------------
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    y_train_fine = keras.utils.to_categorical(y_train, num_fine)
    y_test_fine = keras.utils.to_categorical(y_test, num_fine)

    x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.
    x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.
    #---------------- data preprocessiong -------------------
    x_train = (x_train-np.mean(x_train)) / np.std(x_train)
    x_test = (x_test-np.mean(x_test)) / np.std(x_test)
    #---------------------- make coarse 2 labels --------------------------
    fine_coarse2 = {0:0, 1:1, 2:0, 3:2, 4:3, 5:5, 6:0, 7:5, 8:4, 9:5}
    y_train_coarse2 = np.zeros((y_train_fine.shape[0], num_coarse_2)).astype("float32")
    y_test_coarse2 = np.zeros((y_test_fine.shape[0], num_coarse_2)).astype("float32")
    for i in range(y_train_coarse2.shape[0]):
      y_train_coarse2[i][fine_coarse2[np.argmax(y_train_fine[i])]] = 1.0
    for i in range(y_test_coarse2.shape[0]):
      y_test_coarse2[i][fine_coarse2[np.argmax(y_test_fine[i])]] = 1.0
    #---------------------- make coarse 1 labels --------------------------
    coarse2_coarse1 = {0:0, 1:0, 2:0, 3:0, 4:1, 5:1}
    y_train_coarse1 = np.zeros((y_train_coarse2.shape[0], num_coarse_1)).astype("float32")
    y_test_coarse1 = np.zeros((y_test_coarse2.shape[0], num_coarse_1)).astype("float32")
    for i in range(y_train_coarse1.shape[0]):
      y_train_coarse1[i][coarse2_coarse1[np.argmax(y_train_coarse2[i])]] = 1.0
    for i in range(y_test_coarse1.shape[0]):
      y_test_coarse1[i][coarse2_coarse1[np.argmax(y_test_coarse2[i])]] = 1.0

    tree = DatasetTree([coarse2_coarse1, fine_coarse2])

    return x_train, y_train_coarse1, y_train_coarse2, y_train_fine, x_test, y_test_coarse1, y_test_coarse2, y_test_fine, tree


def CIFAR10():
    CIFAR10 = keras.datasets.cifar10
    (x_train, y_train), (x_test, y_test) = CIFAR10.load_data()
    #--- coarse 1 classes ---
    num_coarse_1 = 2
    #--- coarse 2 classes ---
    num_coarse_2 = 7
    #--- fine classes ---
    num_fine  = 10

    #-------------------- data loading ----------------------
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    y_train_fine = keras.utils.to_categorical(y_train, num_fine)
    y_test_fine = keras.utils.to_categorical(y_test, num_fine)

    #---------------- data preprocessiong -------------------
    x_train = (x_train-np.mean(x_train)) / np.std(x_train)
    x_test = (x_test-np.mean(x_test)) / np.std(x_test)

    #---------------------- make coarse 2 labels --------------------------
    fine_coarse2 = {
      2:3, 3:5, 5:5,
      1:2, 7:6, 4:6,
      0:0, 6:4, 8:1, 9:2
    }
    y_train_coarse2 = np.zeros((y_train_fine.shape[0], num_coarse_2)).astype("float32")
    y_test_coarse2 = np.zeros((y_test_fine.shape[0], num_coarse_2)).astype("float32")
    for i in range(y_train_coarse2.shape[0]):
      y_train_coarse2[i][fine_coarse2[np.argmax(y_train_fine[i])]] = 1.0
    for i in range(y_test_coarse2.shape[0]):
      y_test_coarse2[i][fine_coarse2[np.argmax(y_test_fine[i])]] = 1.0
      
    #---------------------- make coarse 1 labels --------------------------
    coarse2_coarse1 = {
      0:0, 1:0, 2:0,
      3:1, 4:1, 5:1, 6:1
    }
    y_train_coarse1 = np.zeros((y_train_coarse2.shape[0], num_coarse_1)).astype("float32")
    y_test_coarse1 = np.zeros((y_test_coarse2.shape[0], num_coarse_1)).astype("float32")
    for i in range(y_train_coarse1.shape[0]):
      y_train_coarse1[i][coarse2_coarse1[np.argmax(y_train_coarse2[i])]] = 1.0
    for i in range(y_test_coarse1.shape[0]):
      y_test_coarse1[i][coarse2_coarse1[np.argmax(y_test_coarse2[i])]] = 1.0

    tree = DatasetTree([coarse2_coarse1, fine_coarse2])

    return x_train, y_train_coarse1, y_train_coarse2, y_train_fine, x_test, y_test_coarse1, y_test_coarse2, y_test_fine, tree
  
  
    
def CIFAR100():
    CIFAR100 = keras.datasets.cifar100

    (x_train, y_train), (x_test, y_test) = CIFAR100.load_data(label_mode='fine')
    #--- coarse 1 classes ---
    num_coarse_1 = 8
    #--- coarse 2 classes ---
    num_coarse_2 = 20
    #--- fine classes ---
    num_fine  = 100

    #-------------------- data loading ----------------------
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    y_train_fine = keras.utils.to_categorical(y_train, num_fine)
    y_test_fine = keras.utils.to_categorical(y_test, num_fine)

    #---------------- data preprocessiong -------------------
    x_train = (x_train-np.mean(x_train)) / np.std(x_train)
    x_test = (x_test-np.mean(x_test)) / np.std(x_test)

    fine_coarse2 = {
    0:4,1:1,2:14,3:8,4:0,5:6,6:7,7:7,8:18,9:3,
    10:3,11:14,12:9,13:18,14:7,15:11,16:3,17:9,18:7,19:11,
    20:6,21:11,22:5,23:10,24:7,25:6,26:13,27:15,28:3,29:15,
    30:0,31:11,32:1,33:10,34:12,35:14,36:16,37:9,38:11,39:5,
    40:5,41:19,42:8,43:8,44:15,45:13,46:14,47:17,48:18,49:10,
    50:16,51:4,52:17,53:4,54:2,55:0,56:17,57:4,58:18,59:17,
    60:10,61:3,62:2,63:12,64:12,65:16,66:12,67:1,68:9,69:19,
    70:2,71:10,72:0,73:1,74:16,75:12,76:9,77:13,78:15,79:13,
    80:16,81:19,82:2,83:4,84:6,85:19,86:5,87:5,88:8,89:19,
    90:18,91:1,92:2,93:15,94:6,95:0,96:17,97:8,98:14,99:13
    }
    y_train_coarse2 = np.zeros((y_train_fine.shape[0], num_coarse_2)).astype("float32")
    y_test_coarse2 = np.zeros((y_test_fine.shape[0], num_coarse_2)).astype("float32")
    for i in range(y_train_coarse2.shape[0]):
      y_train_coarse2[i][fine_coarse2[np.argmax(y_train_fine[i])]] = 1.0
    for i in range(y_test_coarse2.shape[0]):
      y_test_coarse2[i][fine_coarse2[np.argmax(y_test_fine[i])]] = 1.0
      
    #---------------------- make coarse 1 labels --------------------------
    coarse2_coarse1 = {
      0:0, 1:0, 2:1, 3:2, 
      4:1, 5:2, 6:2, 7:3, 
      8:4, 9:5, 10:5, 11:4, 
      12:4, 13:3, 14:6, 15:4, 
      16:4, 17:1, 18:7, 19:7
    }
    y_train_coarse1 = np.zeros((y_train_coarse2.shape[0], num_coarse_1)).astype("float32")
    y_test_coarse1 = np.zeros((y_test_coarse2.shape[0], num_coarse_1)).astype("float32")
    for i in range(y_train_coarse1.shape[0]):
      y_train_coarse1[i][coarse2_coarse1[np.argmax(y_train_coarse2[i])]] = 1.0
    for i in range(y_test_coarse1.shape[0]):
      y_test_coarse1[i][coarse2_coarse1[np.argmax(y_test_coarse2[i])]] = 1.0
      
    tree = DatasetTree([coarse2_coarse1, fine_coarse2])

    # return x_train, y_train_coarse1, y_train_coarse2, y_train_fine, x_test, y_test_coarse1, y_test_coarse2, y_test_fine, tree
    return {'x_train':x_train, 'y_train_coarse':y_train_coarse1, 'y_train_medium':y_train_coarse2, 'y_train_fine':y_train_fine, 'x_test':x_test, 'y_test_coarse':y_test_coarse1, 'y_test_medium':y_test_coarse2, 'y_test_fine':y_test_fine, 'tree':tree}
    
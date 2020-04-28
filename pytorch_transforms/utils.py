from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, random_split
import torchvision
from torchvision import transforms
from torchvision.datasets import ImageFolder
from efficientnet_pytorch import EfficientNet
from sklearn.metrics import classification_report, accuracy_score
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
import time

def get_dataset(tfms_list=list(), model_name="b0"):
    resolution = EfficientNet.get_image_size("efficientnet-" + model_name)
    tfms = transforms.Compose([transforms.Resize(resolution),
                               transforms.CenterCrop(resolution)]
                              + tfms_list)
    cal_tech101 = ImageFolder(
        root = "/home/loc/projects/efficient_net/data/101_ObjectCategories",
        transform = tfms
    )
    # Train 60%, val 20%, test 20%
    train_size = int(0.6 * len(cal_tech101))
    test_size = int(0.2 * len(cal_tech101))
    val_size = len(cal_tech101) - train_size - test_size
    train_data, val_data, test_data = random_split(cal_tech101, [train_size, val_size, test_size])
    return train_data, val_data, test_data


class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()
    def reset(self):
        self.val, self.avg, self.sum, self.count = 0, 0, 0, 0
    def update(self, val, n=1):
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
        
loss_list, accuracy_list = list(), list()
        
def plot_graph():
    plt.figure(figsize=(15, 4))
    plt.subplot(121)
    plt.plot(range(len(loss_list)), loss_list, color="green")
    plt.xticks(range(len(loss_list)))
    plt.ylabel("LOSS")
    plt.xlabel("Recorded after every 1 epoch")
    plt.subplot(122)
    plt.plot(range(len(accuracy_list)), accuracy_list, color="orange")
    plt.xticks(range(len(loss_list)))
    plt.ylabel("ACCURACY")
    plt.xlabel("Recorded after every 1 epoch")
    plt.ylim(0,1)
    plt.show()
    
    
def train(model, train_data, val_data, epochs, batch_size):
    optim = torch.optim.Adam(model.parameters())
    loss_list.clear()
    accuracy_list.clear()
    criterion = nn.CrossEntropyLoss().to(device)
    model.to(device)
    model.train()
    dataloader = DataLoader(train_data, batch_size, shuffle=True)
    loss_meter = AverageMeter()
    
    for epoch in range(epochs):
        t = time.time()
        for batch_idx, (inputs, targets) in enumerate(dataloader):
            optim.zero_grad()
            outputs = model(inputs.to(device))
            loss = criterion(outputs, targets.to(device))
            loss.backward()
            optim.step()
            
        accuracy = evaluate(model, val_data, batch_size)
        accuracy_list.append(accuracy)
        loss_list.append(loss.item())
        exe_time = int(time.time()-t)
        print(f"EPOCH: {epoch:>2}, TRAIN_LOSS: {loss.item():.5f}, VAL_ACCU: {accuracy:.4f}, EXE TIME: {exe_time:>3}s")

def evaluate(model, data, batch_size=32, print_accu=False):  
    model.eval()
    accuracy_meter = AverageMeter()
    dataloader = DataLoader(data, batch_size, shuffle=False)
    with torch.no_grad():
        for batch_idx, (inputs, targets) in enumerate(dataloader): 
            outputs = model(inputs.to(device))
            outputs = torch.topk(outputs, k=1).indices.squeeze(0).flatten().cpu().tolist()
            targets = targets.flatten().cpu().tolist()
            accuracy_meter.update(accuracy_score(outputs, targets), len(targets))
    model.train()
    if print_accu:
        percentage = accuracy_meter.avg*100
        print(f"VALIDATE ACCURACY: {percentage:.2f}%")
    else:
        return accuracy_meter.avg
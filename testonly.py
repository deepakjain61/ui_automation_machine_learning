import torch
import numpy as np
from torchvision import datasets
import torchvision.transforms as transforms
from torch.utils.data.sampler import SubsetRandomSampler
from PIL import Image
batch_size = 2
test_size = 0.3
valid_size = 0.1

transform = transforms.Compose([transforms.RandomHorizontalFlip(), transforms.RandomRotation(20), transforms.Resize(size=(224,224)), transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
data = datasets.ImageFolder('test5', transform = transform)

num_data = len(data)
indices_data = list(range(num_data))
np.random.shuffle(indices_data)
split_tt = int(np.floor(test_size * num_data))
train_idx, test_idx = indices_data[split_tt:], indices_data[:split_tt]
test_idx = indices_data[:]
num_train = len(train_idx)
indices_train = list(range(num_train))
np.random.shuffle(indices_train)
split_tv = int(np.floor(valid_size * num_train))
train_new_idx, valid_idx = indices_train[split_tv:],indices_train[:split_tv]

train_sampler = SubsetRandomSampler(train_new_idx)
test_sampler = SubsetRandomSampler(test_idx)
valid_sampler = SubsetRandomSampler(valid_idx)

train_loader = torch.utils.data.DataLoader(data, batch_size=batch_size, sampler=train_sampler, num_workers=1)
valid_loader = torch.utils.data.DataLoader(data, batch_size=batch_size, sampler=valid_sampler, num_workers=1)
test_loader = torch.utils.data.DataLoader(data, sampler = test_sampler, num_workers=1)
classes = [0,1,2,3,4]

import torch.nn as nn
import torch.nn.functional as F
train_on_gpu = torch.cuda.is_available()
import torch.optim as optim
criterion = torch.nn.CrossEntropyLoss()
#optimizer = torch.optim.SGD(model.parameters(), lr = 0.003, momentum= 0.9)
#optimizer = torch.optim.Adam(model.parameters(), lr = 0.005)
n_epochs = 100 # you may increase this number to train a final model
valid_loss_min = np.Inf # track change in validation loss

test_loss = 0.0
class_correct = list(0. for i in range(5))
class_total = list(0. for i in range(5))

import torch.nn as nn
import torch.nn.functional as F
train_on_gpu = torch.cuda.is_available()
# define the CNN architecture
class Net(nn.Module):
  def __init__(self):
    super(Net, self).__init__()

    self.conv1 = nn.Conv2d(3, 32, 5, padding=2)
    self.pool = nn.MaxPool2d(5, 5)
    self.conv2 = nn.Conv2d(32, 64, 5, padding=2)
    self.conv3 = nn.Conv2d(64, 32, 5, padding=2)

    self.dropout = nn.Dropout(0.2)
    self.fc1 = nn.Linear(32*1*1, 128)
    self.fc2 = nn.Linear(128, 5)
    self.softmax = nn.LogSoftmax(dim=1)

  def forward(self, x):
    #print(x.size())
    x = self.pool(F.relu(self.conv1(x)))
    #print(x.size())
    x = self.pool(F.relu(self.conv2(x)))
    #print(x.size())
    x = self.pool(F.relu(self.conv3(x)))
    #print(x.size())
    x = self.dropout(x)

    x = x.view(-1, 32 * 1 * 1)
    x = F.relu(self.fc1(x))
    x = self.softmax(self.fc2(x))
    #print(x.size())
    return x
model = Net()
model.load_state_dict(torch.load("uitest_model.pt"))
model.eval()

for data, target in test_loader:
    output = model(data)
    a = output.tolist()
    result = a[0].index(max(a[0]))

print(result)


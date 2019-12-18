import torch
import numpy as np
from torchvision import datasets
import torchvision.transforms as transforms
from torch.utils.data.sampler import SubsetRandomSampler

batch_size = 2
test_size = 0.3
valid_size = 0.1

transform = transforms.Compose([transforms.RandomHorizontalFlip(), transforms.RandomRotation(20), transforms.Resize(size=(224,224)), transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
data = datasets.ImageFolder('augmented_data', transform = transform)

num_data = len(data)
indices_data = list(range(num_data))
np.random.shuffle(indices_data)
split_tt = int(np.floor(test_size * num_data))
train_idx, test_idx = indices_data[split_tt:], indices_data[:split_tt]

num_train = len(train_idx)
indices_train = list(range(num_train))
np.random.shuffle(indices_train)
split_tv = int(np.floor(valid_size * num_train))
train_new_idx, valid_idx = indices_train[split_tv:], indices_train[:split_tv]

train_sampler = SubsetRandomSampler(train_new_idx)
test_sampler = SubsetRandomSampler(test_idx)
valid_sampler = SubsetRandomSampler(valid_idx)

train_loader = torch.utils.data.DataLoader(data, batch_size=batch_size, sampler=train_sampler, num_workers=1)
valid_loader = torch.utils.data.DataLoader(data, batch_size=batch_size, sampler=valid_sampler, num_workers=1)
test_loader = torch.utils.data.DataLoader(data, sampler = test_sampler, batch_size=batch_size, num_workers=1)
classes = [0,1,2,3,4]

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
import torch.optim as optim
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr = 0.003, momentum= 0.9)
#optimizer = torch.optim.Adam(model.parameters(), lr = 0.005)
n_epochs = 1000 # you may increase this number to train a final model
valid_loss_min = np.Inf # track change in validation loss

for epoch in range(1, n_epochs+1):
  train_loss = 0.0
  valid_loss = 0.0
  model.train()
  for data, target in train_loader:
    optimizer.zero_grad()
    output = model(data)
    print(output)
    print(target)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()
    train_loss += loss.item()*data.size(0)
    model.eval() 
  for data, target in valid_loader:
    output = model(data)
    loss = criterion(output, target)
    valid_loss += loss.item()*data.size(0)
  train_loss = train_loss/len(train_loader.dataset)
  valid_loss = valid_loss/len(valid_loader.dataset)
  print('Epoch: {} \tTraining Loss: {:.6f} \tValidation Loss: {:.6f}'.format(epoch, train_loss, valid_loss))
  if valid_loss <= valid_loss_min:
    print('Validation loss decreased ({:.6f} --> {:.6f}).  Saving model ...'.format(valid_loss_min, valid_loss))
    torch.save(model.state_dict(), 'model_cifar.pt')
    valid_loss_min = valid_loss

test_loss = 0.0
class_correct = list(0. for i in range(5))
class_total = list(0. for i in range(5))

model.eval()
i=1
for data, target in test_loader:
  i=i+1
  if len(target)!=batch_size:
    continue
  output = model(data)
  print(output)
  print(target)
  loss = criterion(output, target)
  test_loss += loss.item()*data.size(0)
  _, pred = torch.max(output, 1)    
  correct_tensor = pred.eq(target.data.view_as(pred))
  correct = np.squeeze(correct_tensor.numpy()) if not train_on_gpu else np.squeeze(correct_tensor.cpu().numpy())
  for i in range(batch_size):       
    label = target.data[i]
    class_correct[label] += correct[i].item()
    class_total[label] += 1
test_loss = test_loss/len(test_loader.dataset)
print('Test Loss: {:.6f}\n'.format(test_loss))

print(len(class_total))
print(len(class_correct))
for i in range(5):
  if class_total[i] > 0:
    print('Test Accuracy of %5s: %2d%% (%2d/%2d)' % (classes[i], 100 * class_correct[i] / class_total[i], np.sum(class_correct[i]), np.sum(class_total[i])))
  else:
    print('Test Accuracy of %5s: N/A (no training examples)' % (classes[i]))
print('\nTest Accuracy (Overall): %2d%% (%2d/%2d)' % (100. * np.sum(class_correct) / np.sum(class_total), np.sum(class_correct), np.sum(class_total)))


import torch
from torchvision import datasets
import torchvision.transforms as transforms
from torch.utils.data.sampler import SubsetRandomSampler
import torch.nn as nn
import torch.nn.functional as F

page_map = {
  0: "Create Views",
  1: "Dashboard",
  2: "Login",
  3: "Views",
  4: "View_Details"
}


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

def classify_webpage():
  input_image_path = "model"
  transform = transforms.Compose([transforms.RandomHorizontalFlip(), transforms.RandomRotation(20), transforms.Resize(size=(224,224)), transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
  data = datasets.ImageFolder(input_image_path, transform = transform)
  num_data = len(data)
  indices_data = list(range(num_data))
  test_idx = indices_data[:]
  test_sampler = SubsetRandomSampler(test_idx)
  test_loader = torch.utils.data.DataLoader(data, sampler=test_sampler, num_workers=1)
  model = Net()
  model.load_state_dict(torch.load("uitest_model.pt"))
  model.eval()
  for data, target in test_loader:
      output = model(data)
      print output
      a = output.tolist()
      result = a[0].index(max(a[0]))

  print "The image present at location {} is classified as {}".format(input_image_path, page_map[result])
  return page_map[result]

